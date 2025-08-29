import React, { useState } from "react";
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
}

const GraphComponent: React.FC<GraphComponentProps> = ({
  graphs,
  isCollapsed = false,
  onToggleCollapse,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const plotData = graphs.map((graph, index) => ({
    x: graph.x_data,
    y: graph.y_data,
    type: "scatter" as const,
    mode: "lines+markers",
    name: graph.marker_name,
    marker: { color: `hsl(${(index * 360) / graphs.length}, 70%, 50%)` },
  }));

  const layout = {
    width: 400,
    height: 300,
    title: "Test Data Graph",
    showlegend: true,
  };

  const fullScreenLayout = {
    width: window.innerWidth * 0.9,
    height: window.innerHeight * 0.9,
    title: "Test Data Graph",
    showlegend: true,
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
        style={{
          position: "relative",
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "3px",
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
        <Plot
          data={plotData}
          layout={layout}
          config={{ displayModeBar: false, displaylogo: false }}
        />
      </div>

      <Dialog
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Graph View"
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
              modeBarButtonsToAdd: ["toggleHover", "resetScale2d"],
              modeBarButtonsToRemove: [
                "pan2d",
                "select2d",
                "lasso2d",
                "autoScale2d",
              ],
            }}
          />
        </div>
        <div className="bp4-dialog-footer">
          <Button onClick={() => setIsModalOpen(false)}>Close</Button>
        </div>
      </Dialog>
    </>
  );
};

export default GraphComponent;
