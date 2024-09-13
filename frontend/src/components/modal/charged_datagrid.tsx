// mui
import { Stack, Typography } from "@mui/material";
import {
  GridColDef,
  GridRowsProp,
  GridToolbarColumnsButton,
  GridToolbarContainer,
  GridToolbarFilterButton,
} from "@mui/x-data-grid";
// components
import AppDataGrid from "@/components/AppDataGrid";
import { AccruedCharge } from "@/app/slices/types";

type Props = {
  chargeData: AccruedCharge[];
  chargeStatus: string;
  shipmentNumber: string;
};

function ChargedDataGrid({ chargeData, chargeStatus, shipmentNumber }: Props) {
  const headerClassName = "items-in-progress";

  const columns: GridColDef[] = [
    {
      field: "charge_code",
      headerName: "Charge Code",
      headerClassName,
      flex: 1,
    },
    {
      field: "description",
      headerName: "Description",
      headerClassName,
      flex: 1,
    },
    {
      field: "charge_amount",
      headerName: "Charge Amount",
      headerClassName,
      flex: 1,
    },
    {
      field: "currency",
      headerName: "Currency",
      headerClassName,
      flex: 1,
    },
    {
      field: "is_posted",
      headerName: "Is Posted",
      headerClassName,
      flex: 1,
    },
    {
      field: "creditor",
      headerName: "Creditor",
      headerClassName,
      flex: 1,
    },
    {
      field: "display_sequence",
      headerName: "Display Sequence",
      headerClassName,
      flex: 1,
    },
    {
      field: "ap_invoice_number",
      headerName: "Ap Invoice Number",
      headerClassName,
      flex: 1,
    },
  ];

  const rows: GridRowsProp = chargeData
    ? chargeData.map((item: AccruedCharge, index: number) => ({
      id: index,
      ...item,
    }))
    : [];

  const toolbar = () => (
    <GridToolbarContainer
      sx={{ justifyContent: "space-between", p: 1, color: "#19857b" }}
    >
      <Typography variant="h6" color="primary" sx={{ flexGrow: 1 }}>
        Shipment Number: {shipmentNumber}
      </Typography>
      <Stack direction="row">
        <GridToolbarColumnsButton slotProps={{ button: { color: "info" } }} />
        <GridToolbarFilterButton slotProps={{ button: { color: "info" } }} />
      </Stack>
    </GridToolbarContainer>
  );

  return (
    <Stack>
    <AppDataGrid
      columns={columns}
      rows={rows}
      loading={chargeStatus === "loading" ? true : false}
      headerClassName={headerClassName}
      toolbar={toolbar}
    />
    </Stack>
  );
  
}

export default ChargedDataGrid;
