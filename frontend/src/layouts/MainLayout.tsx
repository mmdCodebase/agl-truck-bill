import * as React from "react";
import { Outlet } from "react-router-dom";
import { styled, useTheme, Theme, CSSObject } from "@mui/material/styles";
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
// mui
import {
  Box,
  CssBaseline,
  Divider,
  IconButton,
  Link,
  List,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import MuiAppBar, { AppBarProps as MuiAppBarProps } from "@mui/material/AppBar";
import MuiDrawer from "@mui/material/Drawer";
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Menu as MenuIcon,
  DashboardOutlined as DashboardIcon,
  TableViewOutlined as TableViewIcon,
} from "@mui/icons-material";
// components
import NavItem from "@/components/NavItem";
import { useColorModeContext } from "../theme";

const drawerWidth = 240;

const openedMixin = (theme: Theme): CSSObject => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme: Theme): CSSObject => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up("sm")]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

interface AppBarProps extends MuiAppBarProps {
  open?: boolean;
}

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})<AppBarProps>(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  ...(open && {
    ...openedMixin(theme),
    "& .MuiDrawer-paper": openedMixin(theme),
  }),
  ...(!open && {
    ...closedMixin(theme),
    "& .MuiDrawer-paper": closedMixin(theme),
  }),
}));

export default function MainLayout() {
  const theme = useTheme();
  const colorMode = useColorModeContext();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };
  return (
    <Box sx={{ display: "flex"}}>
      <CssBaseline />
      <AppBar position="fixed" open={open} style={{backgroundColor:theme.palette.mode === 'dark'?'rgb(10,10,10)':'rgb(26,32,56)',borderBottom:theme.palette.mode === 'dark'?'2px solid white':'2px solid black'}}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{
              marginRight: 5,
              color:theme.palette.mode === 'dark'?'white':'black',
              ...(open && { display: "none" }),
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer variant="permanent" open={open} sx={{
        ".MuiDrawer-paper" :{
          backgroundColor: theme.palette.mode ==='dark'?'rgb(30,30,30)':'white'
        }
      }}>
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "rtl" ? (
              <ChevronRightIcon />
            ) : (
              <ChevronLeftIcon />
            )}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
          <Link href="/" underline="none">
            {open ? (
              <NavItem
                open={open}
                path="/dashboard"
                itemText="Dashboard"
                itemIcon={<DashboardIcon />}
              />
            ) : (
              <Tooltip title="Dashboard" placement="right" arrow>
                <NavItem
                  open={open}
                  path="/dashboard"
                  itemText="Dashboard"
                  itemIcon={<DashboardIcon />}
                />
              </Tooltip>
            )}
          </Link>
          <Link href="/all-data" underline="none">
            {open ? (
              <NavItem
                open={open}
                path="/all-data"
                itemText="All Data"
                itemIcon={<TableViewIcon />}
              />
            ) : (
              <Tooltip title="All Data" placement="right" arrow>
                <NavItem
                  open={open}
                  path="/all-data"
                  itemText="All Data"
                  itemIcon={<TableViewIcon />}
                />
              </Tooltip>
            )}
          </Link>
        </List>
        <IconButton sx={{ mt: 'auto', outline:'none', border:'0px solid white' }} onClick={() => colorMode.toggleColorMode()} color="inherit" >
          {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, p: 2, pt: 10, bgcolor: "white", minHeight: "100vh", backgroundColor:theme.palette.mode === 'dark'?'rgb(40,40,40)':'white' }}
      >
        <Outlet />
      </Box>
    </Box>
  );
}
