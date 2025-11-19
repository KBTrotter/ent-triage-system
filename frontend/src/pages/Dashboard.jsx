import React from "react";
import {
  Grid,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import DataGrid from "../components/grid/DataGrid";
import mockData from "../../mockData/triageCaseMockData.json";
import { triageCaseColumnDefs } from "../constants/triageCase";
import { STATUS_VALUES, STATUS_LABELS } from "../constants/consts";

export default function Dashboard() {
  const [selectedStatus, setSelectedStatus] = React.useState(STATUS_LABELS[STATUS_VALUES.PENDING]);
  const unresolvedCases = mockData.triageCases.filter((c) => c.status === STATUS_VALUES.PENDING);
  const resolvedCases = mockData.triageCases.filter((c) => c.status === STATUS_VALUES.RESOLVED);

  const handleChange = (event) => {
    const value = event.target.value;
    setSelectedStatus(value);
  };

  return (
    <Grid container spacing={2} m={2}>
      <Grid size={12}>
        <Typography variant="h4">Dashboard</Typography>
      </Grid>
      <Grid size={12}>
        <FormControl fullWidth size="small">
          <InputLabel id="status-label">Status</InputLabel>
          <Select
            labelId="status-label"
            value={selectedStatus}
            onChange={handleChange}
            label="Status"
          >
            {Object.values(STATUS_LABELS).map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid size={12} sx={{ height: "60vh" }}
      >
        <DataGrid
          rowData={selectedStatus === STATUS_LABELS[STATUS_VALUES.PENDING] ? unresolvedCases : resolvedCases}
          columnDefs={triageCaseColumnDefs}
        />
      </Grid>
    </Grid>
  );
}
