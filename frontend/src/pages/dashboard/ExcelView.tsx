// mui
import { Button, Stack } from "@mui/material";
import {
  GridColDef,
  GridRowsProp,
  GridToolbarColumnsButton,
  GridToolbarContainer,
  GridToolbarFilterButton,
} from "@mui/x-data-grid";
// components
import AppDataGrid from "@/components/AppDataGrid";
import { CWDataResponse } from "@/app/slices/types";

type Props = {
  cwData: CWDataResponse[];
  cwStatus: string;
  downloadCWUploadTemplate: () => void;
};

function ExcelView({ cwData, cwStatus, downloadCWUploadTemplate }: Props) {
  const headerClassName = "items-in-progress";

  const columns: GridColDef[] = [
    {
      field: "agl_shipment_number",
      headerName: "SHIPMENT ID",
      headerClassName,
      flex: 1,
    },
    {
      field: "updated_at",
      headerName: "Updated At",
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
      field: "invoice_num",
      headerName: "Invoice Num",
      headerClassName,
      flex: 1,
    },
    {
      field: "invoice_date",
      headerName: "Invoice Date",
      headerClassName,
      flex: 1,
    },
    {
      field: "supplier_cost_ref",
      headerName: "Supplier Cost Ref",
      headerClassName,
      flex: 1,
    },
    {
      field: "ar_ap",
      headerName: "Is AR or AP",
      headerClassName,
      flex: 1,
    },
    {
      field: "is_post",
      headerName: "IsPost(Y/N)",
      headerClassName,
      flex: 1,
    },
    {
      field: "FRT",
      headerName: "FRT",
      headerClassName,
      flex: 1,
    },
    {
      field: "AGEN",
      headerName: "AGEN",
      headerClassName,
      flex: 1,
    },
    {
      field: "AMS",
      headerName: "AMS",
      headerClassName,
      flex: 1,
    },
    {
      field: "EQUIP",
      headerName: "EQUIP",
      headerClassName,
      flex: 1,
    },
    {
      field: "ORIGIN",
      headerName: "ORIGIN",
      headerClassName,
      flex: 1,
    },
    {
      field: "LOCAL",
      headerName: "LOCAL",
      headerClassName,
      flex: 1,
    },
    {
      field: "PP",
      headerName: "PP",
      headerClassName,
      flex: 1,
    },
    {
      field: "TERFEE",
      headerName: "TERFEE",
      headerClassName,
      flex: 1,
    },
    {
      field: "TELEX",
      headerName: "TELEX",
      headerClassName,
      flex: 1,
    },
    {
      field: "VGM",
      headerName: "VGM",
      headerClassName,
      flex: 1,
    },
    {
      field: "DCART",
      headerName: "DCART",
      headerClassName,
      flex: 1,
    },
    {
      field: "SEAL",
      headerName: "SEAL",
      headerClassName,
      flex: 1,
    },
    {
      field: "DOC",
      headerName: "DOC",
      headerClassName,
      flex: 1,
    },
    {
      field: "BOOK",
      headerName: "BOOK",
      headerClassName,
      flex: 1,
    },
    {
      field: "CCLR",
      headerName: "CCLR",
      headerClassName,
      flex: 1,
    },
    {
      field: "ALINE",
      headerName: "ALINE",
      headerClassName,
      flex: 1,
    },
    {
      field: "PSEC",
      headerName: "PSEC",
      headerClassName,
      flex: 1,
    },
    {
      field: "EGF",
      headerName: "EGF",
      headerClassName,
      flex: 1,
    },
    {
      field: "TRANS",
      headerName: "TRANS",
      headerClassName,
      flex: 1,
    },
    {
      field: "CHRENT",
      headerName: "CHRENT",
      headerClassName,
      flex: 1,
    },
  ];

  const rows: GridRowsProp = cwData
    ? cwData.map((item: CWDataResponse, index: number) => ({
        id: index,
        ...item,
      }))
    : [];

  const toolbar = () => (
    <GridToolbarContainer
      sx={{ justifyContent: "space-between", p: 1, color: "#19857b" }}
    >
      <Stack direction="row">
        <GridToolbarColumnsButton slotProps={{ button: { color: "info" } }} />
        <GridToolbarFilterButton slotProps={{ button: { color: "info" } }} />
      </Stack>
      <Button color="info" onClick={downloadCWUploadTemplate}>
        Download as CW Upload template
      </Button>
    </GridToolbarContainer>
  );

  return (
    <AppDataGrid
      columns={columns}
      rows={rows}
      loading={cwStatus === "loading" ? true : false}
      headerClassName={headerClassName}
      toolbar={toolbar}
    />
  );
}

export default ExcelView;
