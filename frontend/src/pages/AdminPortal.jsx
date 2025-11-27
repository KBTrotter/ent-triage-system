import Navbar from "../components/Navbar";
import React, { useState } from "react";
import { Grid, Typography, Button } from "@mui/material";
import DataGrid from "../components/grid/DataGrid";
import mockData from "../../mockData/userMockData.json";
import { userColumnDefs } from "../utils/coldefs/user";
import CreateUserDialog from "../components/admin/CreateUserDialog";

export default function AdminPortal() {
  const [createUserOpen, setCreateUserOpen] = useState(false);

  const handleCreateUser = (userData) => {
    console.log("Creating user:", userData);
    // TODO: api call
    setCreateUserOpen(false);
  };

  return (
    <>
      <Navbar />
      <Grid container spacing={2} p={2}>
        <Grid size={6}>
          <Typography variant="h4">Admin</Typography>
        </Grid>
        <Grid size={6} sx={{ display: "flex", justifyContent: "flex-end" }}>
          <Button
            variant="contained"
            onClick={() => setCreateUserOpen(true)}
          >
            Create User
          </Button>
        </Grid>
        <Grid size={12}>
          <Grid size={12} sx={{ height: "75vh" }}>
            <DataGrid rowData={mockData.users} columnDefs={userColumnDefs} />
          </Grid>
        </Grid>
      </Grid>
      <CreateUserDialog
        open={createUserOpen}
        onClose={() => setCreateUserOpen(false)}
        onSave={handleCreateUser}
      />
    </>
  );
}