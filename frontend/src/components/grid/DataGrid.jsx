import React from "react";
import { AgGridReact } from "ag-grid-react";
import { ModuleRegistry, AllCommunityModule } from "ag-grid-community";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";
import "./GridStyles.css";

ModuleRegistry.registerModules([AllCommunityModule]);

const DataGrid = ({ rowData, columnDefs, ...gridOptions }) => {
  const handleGridReady = (params) => {
    params.api.sizeColumnsToFit();
  };

  return (
    <div
      className="ag-theme-material"
      style={{ height: "100%", width: "100%" }}
    >
      <AgGridReact
        theme="legacy"
        rowData={rowData}
        columnDefs={columnDefs}
        onGridReady={handleGridReady}
        tooltipShowDelay={0}
        {...gridOptions}
      />
    </div>
  );
};

export default DataGrid;
