// mui
import { Stack } from "@mui/material";
import {
  GridColDef,
  GridRowsProp,
  GridToolbarColumnsButton,
  GridToolbarContainer,
  GridToolbarFilterButton,
  GridRowParams
} from "@mui/x-data-grid";
// components
import AppDataGrid from "@/components/AppDataGrid";
import { AttachmentDataResponse } from "@/app/slices/types";
import { useAppDispatch } from "@/app/hooks";
import { setAttachmentIndex } from "@/app/slices/email.slice";

type Props = {
  attachmentData: AttachmentDataResponse[];
  attachmentStatus: string;
};

function AttachmentView({ attachmentData, attachmentStatus}: Props) {
  const dispatch = useAppDispatch();
  const headerClassName = "items-in-progress";

  const columns: GridColDef[] = [
    {
      field: "file_name",
      headerName: "File Name",
      headerClassName,
      flex: 1,
    },
    {
      field: "content_type",
      headerName: "Content Type",
      headerClassName,
      flex: 1,
    },
    {
      field: "is_inline",
      headerName: "Is Inline",
      headerClassName,
      flex: 1,
    },
  ];

  const rows: GridRowsProp = attachmentData
    ? attachmentData.map((item: AttachmentDataResponse, index: number) => ({
      id: index, 
        ...item,
      }))
    : [];

  const handleRowClick = (params: GridRowParams) => {
    // Find the index of the clicked row based on the ID
    const index = rows.findIndex(row => row.id === params.id);
    dispatch(setAttachmentIndex(index));

  };
 

  const toolbar = () => (
    <GridToolbarContainer
      sx={{ justifyContent: "space-between", p: 1, color: "#19857b" }}
    >
      <Stack direction="row">
        <GridToolbarColumnsButton slotProps={{ button: { color: "info" } }} />
        <GridToolbarFilterButton slotProps={{ button: { color: "info" } }} />
      </Stack>
    </GridToolbarContainer>
  );

  return (
    <AppDataGrid
      columns={columns}
      rows={rows}
      loading={attachmentStatus === "loading" ? true : false}
      headerClassName={headerClassName}
      toolbar={toolbar}
      onRowClick={handleRowClick}
    />
  );
}

export default AttachmentView;
