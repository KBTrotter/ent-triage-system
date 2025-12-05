import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Avatar,
  Popover,
} from "@mui/material";
import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { deepPurple, grey } from "@mui/material/colors";
import { NAV_PAGES, roleLabel } from "../utils/consts";

export default function Navbar() {
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  // Account Popover user info
  const userRole = user?.role ?? null;
  const userInitial = user?.first_initial ?? "";
  const userFirstName = user?.firstName ?? "";
  const userLastName = user?.lastName ?? "";
  const username = `${userFirstName} ${userLastName}`;

  const handleOpenUserMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleCloseUserMenu = () => {
    setAnchorEl(null);
  };
  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const accountPopoverOpen = Boolean(anchorEl);

  return (
    <AppBar
      position="static"
      sx={{ bgcolor: deepPurple[50], color: grey[900] }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          ENT Triage System
        </Typography>
        {NAV_PAGES.filter((p) => !p.role || p.role === userRole).map(
          ({ label, path }) => (
            <Button key={label} color="inherit" onClick={() => navigate(path)}>
              {label}
            </Button>
          )
        )}
        <IconButton
          size="large"
          edge="end"
          color="inherit"
          onClick={handleOpenUserMenu}>
          <Avatar sx={{ bgcolor: deepPurple[400] }}>{userInitial}</Avatar>
        </IconButton>
        <Popover
          open={accountPopoverOpen}
          anchorEl={anchorEl}
          onClose={handleCloseUserMenu}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          transformOrigin={{ vertical: "top", horizontal: "right" }}>
          <Box display="flex" alignItems="center" p={2} gap={2} minWidth={200}>
            <Avatar sx={{ bgcolor: deepPurple[400] }}>{userInitial}</Avatar>
            <Box>
              <Typography variant="subtitle1">{username}</Typography>
              <Typography variant="body1" color="textSecondary">
                {roleLabel(userRole)}
              </Typography>
            </Box>
          </Box>
          <Box p={2}>
            <Button
              variant="contained"
              sx={{ bgcolor: deepPurple[400], borderRadius: 8 }}
              onClick={handleLogout}
              fullWidth>
              Logout
            </Button>
          </Box>
        </Popover>
      </Toolbar>
    </AppBar>
  );
}
