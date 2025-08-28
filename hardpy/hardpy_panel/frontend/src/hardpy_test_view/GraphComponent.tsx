// GraphComponent.tsx
import React, { useState } from "react";
import { Modal, Button } from "@blueprintjs/core";
import Plot from "react-plotly.js";

interface GraphData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
}

interface GraphComponentProps {
  graphs: GraphData[];
}

const GraphComponent: React.FC<GraphComponentProps> = ({ graphs }) => {
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

  return (
    <>
      <div
        style={{ width: "100%", cursor: "pointer" }}
        onClick={() => setIsModalOpen(true)}
      >
        <Plot
          data={plotData}
          layout={layout}
          config={{ displayModeBar: true, displaylogo: false }}
        />
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Graph View"
        className="graph-modal"
      >
        <div className={Classes.DIALOG_BODY}>
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
        <div className={Classes.DIALOG_FOOTER}>
          <Button onClick={() => setIsModalOpen(false)}>Close</Button>
        </div>
      </Modal>
    </>
  );
};

export default GraphComponent;
