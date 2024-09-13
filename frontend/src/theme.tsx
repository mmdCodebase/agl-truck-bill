import * as React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { red } from "@mui/material/colors";

const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

export default function ColorModeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = React.useState<'light' | 'dark'>('light');
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: {
            main: "#1A2038",
          },
          secondary: {
            main: "#556cd6",
          },
          success:{
            main:"#ffffff"
          },
          error: {
            main: red.A400,
          },
        },
      }),
    [mode],
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        { children }
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export function useColorModeContext() {
  const context = React.useContext(ColorModeContext);
  return context;
}

