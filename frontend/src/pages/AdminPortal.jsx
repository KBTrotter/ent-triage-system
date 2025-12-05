import Navbar from "../components/Navbar";
import React, { useEffect, useState } from "react";
import { Grid, Typography, Button } from "@mui/material";
import DataGrid from "../components/grid/DataGrid";
import { userColumnDefs } from "../utils/coldefs/user";
import CreateUserDialog from "../components/admin/CreateUserDialog";
import { userService } from "../api/userService";

export default function AdminPortal() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [createUserOpen, setCreateUserOpen] = useState(false);
  const [createUserError, setCreateUserError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    const results = await userService.getAllUsers();
    setUsers(results.data);
    setLoading(false);
  };

  const handleCreateUser = async (userData) => {
    try {
      await userService.createUser(userData);
      fetchUsers();
      setCreateUserOpen(false);
      setCreateUserError(null);
    } catch (err) {
      if (err.response?.status === 409) {
        setCreateUserError(
          "Failed to create user: User with this email already exists"
        );
      } else {
        setCreateUserError("Failed to create user, please try again");
      }
    }
  };

  return (
    <>
      <Navbar />
      <Grid container spacing={2} p={2}>
        <Grid size={6}>
          <Typography variant="h4">Admin</Typography>
        </Grid>
        <Grid size={6} sx={{ display: "flex", justifyContent: "flex-end" }}>
          <Button variant="contained" onClick={() => setCreateUserOpen(true)}>
            Create User
          </Button>
        </Grid>
        <Grid size={12}>
          <Grid size={12} sx={{ height: "75vh" }}>
            <DataGrid rowData={users} columnDefs={userColumnDefs(fetchUsers)} />
          </Grid>
        </Grid>
      </Grid>
      <CreateUserDialog
        open={createUserOpen}
        onClose={() => {
          setCreateUserOpen(false);
          setCreateUserError(null);
        }}
        onSave={handleCreateUser}
        error={createUserError}
      />
    </>
  );
}
