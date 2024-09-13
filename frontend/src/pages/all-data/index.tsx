import { useEffect, useState } from "react";
// mui
import {
  Button,
  FormControl,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Stack,
} from "@mui/material";
import {
  GridColDef,
  GridRowsProp,
  GridToolbarColumnsButton,
  GridToolbarContainer,
  GridToolbarFilterButton,
} from "@mui/x-data-grid";
import { Close as CloseIcon } from "@mui/icons-material";
import { SnackbarKey, useSnackbar } from "notistack";
// hooks
import { useAppDispatch, useAppSelector } from "@/app/hooks";
// reducer
import { fetchCWData } from "@/app/slices/data.slice";
// components
import AppDataGrid from "@/components/AppDataGrid";
import { CWDataResponse } from "@/app/slices/types";
import { downloadCWUpload } from "@/app/slices/file.slice";

function AllData() {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const dispatch = useAppDispatch();
  const { cwUploadData, cwUploadDataStatus, cwUploadDataError } =
    useAppSelector((state) => state.data);
  const { downloadCWStatus, downloadCWError } = useAppSelector(
    (state) => state.file
  );

  const [cwStatus, setCWStatus] = useState<string>("CREATED");

  useEffect(() => {
    dispatch(fetchCWData(cwStatus));
  }, [cwStatus]);

  const closeAction = (key: SnackbarKey) => (
    <IconButton
      size="small"
      aria-label="close"
      color="inherit"
      onClick={() => closeSnackbar(key)}
    >
      <CloseIcon fontSize="small" />
    </IconButton>
  );

  useEffect(() => {
    if (cwUploadDataStatus === "succeeded") {
      enqueueSnackbar("Successfully loaded the CW Upload data.", {
        variant: "success",
      });
    } else if (cwUploadDataStatus === "failed") {
      enqueueSnackbar(cwUploadDataError, {
        variant: "error",
        persist: true,
        action: closeAction,
      });
    }
  }, [cwUploadDataStatus]);

  useEffect(() => {
    if (downloadCWStatus === "succeeded") {
      enqueueSnackbar("Successfully downloaded the CW upload excel file.", {
        variant: "success",
      });
    } else if (downloadCWStatus === "failed") {
      enqueueSnackbar(downloadCWError, {
        variant: "error",
        persist: true,
        action: closeAction,
      });
    }
  }, [downloadCWStatus]);

  const downloadCWUploadTemplate = async () => {
    if (!!cwUploadData.length) {
      await dispatch(downloadCWUpload());
      await dispatch(fetchCWData(cwStatus));
    }
  };

  const headerClassName = "all-data";

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

  const rows: GridRowsProp = cwUploadData
    ? cwUploadData.map((item: CWDataResponse, index: number) => ({
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
      <Stack direction="row">
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="cw-status-label">CW Status</InputLabel>
          <Select
            labelId="cw-status-label"
            id="cw-status"
            value={cwStatus}
            label="CW Status"
            size="small"
            onChange={(e) => setCWStatus(e.target.value)}
          >
            <MenuItem value="CREATED">Created</MenuItem>
            <MenuItem value="PENDING_DATA_EXTRACTION">
              Pending data extraction
            </MenuItem>
            <MenuItem value="FAILED">Failed</MenuItem>
            <MenuItem value="READY_FOR_REVIEW">Ready for review</MenuItem>
            <MenuItem value="PENDING_CW_UPLOAD">Pending cw upload</MenuItem>
            <MenuItem value="SKIPPED">Skipped</MenuItem>
            <MenuItem value="DOWNLOADED">Downloaded</MenuItem>
          </Select>
        </FormControl>
        <Button
          color="info"
          onClick={downloadCWUploadTemplate}
          disabled={
            cwStatus === "DOWNLOADED" || cwStatus === "PENDING_CW_UPLOAD"
              ? false
              : true
          }
        >
          Download as CW Upload template
        </Button>
      </Stack>
    </GridToolbarContainer>
  );

  return (
    <AppDataGrid
      columns={columns}
      rows={rows}
      loading={cwUploadDataStatus === "loading" ? true : false}
      headerClassName={headerClassName}
      toolbar={toolbar}
      sx={{ height: 800 }}
    />
  );
}

export default AllData;
