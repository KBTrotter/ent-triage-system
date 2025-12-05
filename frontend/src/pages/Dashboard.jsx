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
import { triageCaseColumnDefs } from "../utils/coldefs/triageCase";
import { ExpandMore } from "@mui/icons-material";
import Navbar from "../components/Navbar";
import { useTriageCases } from "../context/TriageCaseContext";

export default function Dashboard() {
  const { 
    cases,
    loading,
    fetchCases, 
    getUnresolvedCases, 
    getResolvedCases 
  } = useTriageCases();

  React.useEffect(() => {
    const getCases = async () => {
      console.log("Fetching cases");
      await fetchCases();
    };
    getCases();
  }, [fetchCases]);

  const unresolvedCases = React.useMemo(() => {
    return getUnresolvedCases();
  }, [getUnresolvedCases]);

  const resolvedCases = React.useMemo(() => {
    return getResolvedCases();
  }, [getResolvedCases]);

  return (
    <>
      <Navbar />
      <Grid container spacing={2} p={2}>
        <Grid size={12}>
          <Typography variant="h4">Dashboard</Typography>
        </Grid>
        <Grid size={12}>
          <Accordion
            disableGutters
            defaultExpanded
            sx={{ backgroundColor: "grey.100" }}
          >
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography variant="h6">
                Unresolved Cases ({unresolvedCases?.length || 0})
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid size={12} sx={{ height: "75vh" }}>
                <DataGrid
                  rowData={unresolvedCases || []}
                  columnDefs={triageCaseColumnDefs}
                  loading={loading}
                />
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid size={12}>
          <Accordion disableGutters sx={{ backgroundColor: "grey.100" }}>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography variant="h6">
                Resolved Cases ({resolvedCases?.length || 0})
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid size={12} sx={{ height: "80vh" }}>
                <DataGrid
                  rowData={resolvedCases || []}
                  columnDefs={triageCaseColumnDefs}
                  loading={loading}
                />
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Grid>
      </Grid>
    </>
  );
}