import { Link } from "@mui/material";

type Props = {
  fileUrl: string;
  fileName: string;
};

function DownloadLink({ fileUrl, fileName }: Props) {
  return (
    <Link href={fileUrl} download={fileName} color="inherit" underline="hover">
      {fileName}
    </Link>
  );
}

export default DownloadLink;
