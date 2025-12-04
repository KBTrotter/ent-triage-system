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
import { STATUS_VALUES } from "../utils/consts";
import Navbar from "../components/Navbar";
import { useTriageCases } from "../context/TriageCaseContext";

export default function Dashboard() {
  const { fetchCases, getUnresolvedCases, getResolvedCases } = useTriageCases();
  const [cases, setCases] = React.useState([]);

  // MOCK DATA
  // const unresolvedCases = mockData.triageCases.filter(
  //   (c) => c.status === STATUS_VALUES.PENDING
  // );
  // const resolvedCases = mockData.triageCases.filter(
  //   (c) => c.status === STATUS_VALUES.RESOLVED
  // );

  React.useEffect(() => {
    const getCases = async () => {
      console.log("fetching cases");
      try {
        const response = await fetchCases();
        console.log("Cases", response.data.data);
        setCases(response.data.data);
      } catch (err) {
        console.error(err);
      }
    };
    getCases();
  }, []);

  const unresolvedCases = React.useMemo(() => {
    return cases.filter(c => c.status !== 'resolved');
  });

  const resolvedCases = React.useMemo(() => {
    return cases.filter(c => c.status === 'resolved');
  });

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
    </>
  );
}
