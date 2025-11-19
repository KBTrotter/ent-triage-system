import React from "react";
import {
  Grid,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import DataGrid from "../components/grid/DataGrid";
import mockData from "../../mockData/triageCaseMockData.json";
import { triageCaseColumnDefs } from "../utils/triageCase";
import { ExpandMore } from "@mui/icons-material";
import { STATUS_VALUES } from "../constants/consts";

export default function Dashboard() {
  // MOCK DATA
  const unresolvedCases = mockData.triageCases.filter((c) => c.status === STATUS_VALUES.PENDING);
  const resolvedCases = mockData.triageCases.filter((c) => c.status === STATUS_VALUES.RESOLVED);

  return (
    <Grid container spacing={2} p={2}>
      <Grid size={12}>
        <Typography variant="h4">Dashboard</Typography>
      </Grid>
      <Grid size={12}>
        <Accordion
          disableGutters
          defaultExpanded
          sx={{
            backgroundColor: "grey.100",
          }}
        >
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">Unresolved Cases</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid size={12} sx={{ height: "75vh" }}>
              <DataGrid
                rowData={unresolvedCases}
                columnDefs={triageCaseColumnDefs}
              />
            </Grid>
          </AccordionDetails>
        </Accordion>
      </Grid>
      <Grid size={12}>
        <Accordion disableGutters sx={{ backgroundColor: "grey.100" }}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">Resolved Cases</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid size={12} sx={{ height: "80vh" }}>
              <DataGrid
                rowData={resolvedCases}
                columnDefs={triageCaseColumnDefs}
              />
            </Grid>
          </AccordionDetails>
        </Accordion>
      </Grid>
    </Grid>
  );
}
