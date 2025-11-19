import React from "react";
import { Grid, Typography } from "@mui/material";
import DataGrid from "../components/grid/DataGrid";
import mockData from "../../mockData/triageCaseMockData.json";
import { triageCaseColumnDefs } from "../constants/triageCase";

export default function Dashboard() {
  const unresolvedCases = mockData.triageCases.filter(
    (c) => c.status === "pending"
  );
  const resolvedCases = mockData.triageCases.filter(
    (c) => c.status === "resolved"
  );

  return (
    <Grid container spacing={2} m={2}>
      <Grid size={12}>
        <Typography variant="h4">Dashboard</Typography>
      </Grid>
      <Grid
        size={12}
        sx={{
          height: "60vh",
          border: "1px solid #ccc",
          borderRadius: 2,
          padding: 2,
        }}
      >
        <Typography variant="h6">Unresolved</Typography>
        <DataGrid rowData={unresolvedCases} columnDefs={triageCaseColumnDefs} />
      </Grid>
    </Grid>
  );
}
