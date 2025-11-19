import React from "react";
import { AgGridReact } from "ag-grid-react";
import {
  ModuleRegistry,
  AllCommunityModule,
  themeQuartz,
} from "ag-grid-community";
import "./GridStyles.css";
import { deepPurple } from "@mui/material/colors";

ModuleRegistry.registerModules([AllCommunityModule]);

const DataGrid = ({ rowData, columnDefs, gridOptions = [] }) => {
  const theme = themeQuartz.withParams({
    // we can set up a MUI theme to centralize our own custom colors, but for now let's import colors from MUI
    // https://mui.com/material-ui/customization/color/
    headerBackgroundColor: deepPurple[200],
    backgroundColor: deepPurple[50],
    border: true,
    rowHoverColor: deepPurple[100],
  });

  return (
    <AgGridReact
      theme={theme}
      rowData={rowData}
      columnDefs={columnDefs}
      tooltipShowDelay={0}
      enableCellTextSelection={true}
      {...gridOptions}
    />
  );
};

export default DataGrid;
