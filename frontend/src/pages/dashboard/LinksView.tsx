import { Box, Stack, Typography } from "@mui/material";
// components
import DownloadLink from "@/components/DownloadLink";

function LinksView() {
  return (
    <Box>
      <Stack direction="row" spacing={1} alignItems="center">
        <Typography variant="subtitle1">
          Click here to download CW upload file:
        </Typography>
        <DownloadLink
          fileUrl="/path/to/your/file.xlsx"
          fileName="CW1_NewChargeRate_UpSert_20231116_174448_taultman.xlsx"
        />
      </Stack>
      <Stack direction="row" spacing={1} alignItems="center">
        <Typography variant="subtitle1">
          Click here to download paycargo invoices:
        </Typography>
        <DownloadLink
          fileUrl="/path/to/your/file.csv"
          fileName="paycargo_invoices_20231116_174448.csv"
        />
      </Stack>
      <Stack direction="row" spacing={1} alignItems="center">
        <Typography variant="subtitle1">
          Click here to download skipped invoices:
        </Typography>
        <DownloadLink
          fileUrl="/path/to/your/file.csv"
          fileName="skipped_invoices_20231116_174448.csv"
        />
      </Stack>
    </Box>
  );
}

export default LinksView;
