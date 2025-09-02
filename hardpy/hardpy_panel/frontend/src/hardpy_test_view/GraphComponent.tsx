import React, { useState, useRef, useEffect } from "react";
import { Dialog, Button, Icon } from "@blueprintjs/core";
import Plot from "react-plotly.js";

interface GraphData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
}

interface GraphComponentProps {
  graphs: GraphData[];
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
  title?: string;
  xLabel?: string;
  yLabel?: string;
}

const GraphComponent: React.FC<GraphComponentProps> = ({
  graphs,
  isCollapsed = false,
  onToggleCollapse,
  title,
  xLabel,
  yLabel,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 300 });

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.offsetWidth,
          height: 300,
        });
      }
    };

    updateDimensions();
    window.addEventListener("resize", updateDimensions);

    return () => window.removeEventListener("resize", updateDimensions);
  }, []);

  const plotData = graphs.map((graph, index) => ({
    x: graph.x_data,
    y: graph.y_data,
    type: "scatter" as const,
    mode: "lines+markers",
    name: graph.marker_name,
    marker: { color: `hsl(${(index * 360) / graphs.length}, 70%, 50%)` },
  }));

  const layout = {
    width: dimensions.width,
    height: dimensions.height,
    title: title || "Test Data Graph",
    xaxis: {
      title: xLabel || undefined,
    },
    yaxis: {
      title: yLabel || undefined,
    },
    showlegend: true,
    autosize: true,
  };

  const fullScreenLayout = {
    width: window.innerWidth * 0.9,
    height: window.innerHeight * 0.9,
    title: title || "Test Data Graph",
    xaxis: {
      title: xLabel || undefined,
    },
    yaxis: {
      title: yLabel || undefined,
    },
    showlegend: true,
    autosize: true,
  };

  if (isCollapsed) {
    return (
      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "3px",
          background: "#f5f5f5",
        }}
      >
        <Button icon="chevron-down" onClick={onToggleCollapse} minimal small>
          Show graph
        </Button>
      </div>
    );
  }

  return (
    <>
      <div
        ref={containerRef}
        style={{
          position: "relative",
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "3px",
          width: "100%",
          minHeight: "300px",
          minWidth: "300px",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: "10px",
            right: "10px",
            zIndex: 100,
          }}
        >
          <Button
            icon="fullscreen"
            onClick={() => setIsModalOpen(true)}
            minimal
            small
            style={{ marginRight: "5px" }}
          />
          <Button icon="chevron-up" onClick={onToggleCollapse} minimal small />
        </div>
        <div style={{ width: "100%", height: "100%" }}>
          <Plot
            data={plotData}
            layout={layout}
            config={{
              displayModeBar: false,
              displaylogo: false,
              responsive: true,
            }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      </div>

      <Dialog
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={title || "Graph View"}
        className="graph-modal"
        style={{ width: "90vw", height: "90vh" }}
      >
        <div className="bp4-dialog-body">
          <Plot
            data={plotData}
            layout={fullScreenLayout}
            config={{
              displayModeBar: true,
              displaylogo: false,
              responsive: true,
              modeBarButtonsToAdd: ["toggleHover", "resetScale2d"],
              modeBarButtonsToRemove: [
                "pan2d",
                "select2d",
                "lasso2d",
                "autoScale2d",
              ],
            }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      </Dialog>
    </>
  );
};

export default GraphComponent;
