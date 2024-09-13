import { useCallback, useState } from "react";
import {
  ButtonGroup,
  IconButton,
  Pagination,
  Stack,
  Typography,
} from "@mui/material";
import {
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
} from "@mui/icons-material";
import { useResizeObserver } from "@wojtekmaj/react-hooks";
import { pdfjs, Document, Page } from "react-pdf";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "react-pdf/dist/esm/Page/TextLayer.css";
import type { PDFDocumentProxy } from "pdfjs-dist";
// component
import Loading from "@/components/Loading";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

const options = {
  cMapUrl: "/cmaps/",
  standardFontDataUrl: "/standard_fonts/",
};

const resizeObserverOptions = {};

type Props = {
  pdfUrl: string | null;
  pdfStatus: string;
  pdfError: string | null;
  contentType: string | null;
};

function PDFView({ pdfUrl, pdfStatus, pdfError, contentType }: Props) {
  const [numPages, setNumPages] = useState<number>();
  const [page, setPage] = useState<number>(1);
  const [containerRef, setContainerRef] = useState<HTMLElement | null>(null);
  const [scale, setScale] = useState<number>(1);

  const onResize = useCallback<ResizeObserverCallback>((entries) => {
    const [entry] = entries;

    if (entry && containerRef) {
      const { width: containerWidth, height: containerHeight } = entry.contentRect;

      // Calculate the scale to fit both width and height within the container
      const initialScale = Math.min(
        containerWidth / containerRef.offsetWidth,
        containerHeight / containerRef.offsetHeight
      );
      setScale(initialScale);
    }
  }, [containerRef]);

  useResizeObserver(containerRef, resizeObserverOptions, onResize);

  function onDocumentLoadSuccess({
    numPages: nextNumPages,
  }: PDFDocumentProxy): void {
    setNumPages(nextNumPages);
  }
  // @ts-ignore
  const handleChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  const handleZoomIn = () => {
    setScale((prevScale) => Math.min(prevScale + 0.1, 2));
  };

  const handleZoomOut = () => {
    setScale((prevScale) => Math.max(prevScale - 0.1, 0.5));
  };

  return (
    <div className="pdf-viewer" style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <div
        className="pdf-viewer__container"
        style={{ flex: 1, display: "flex", justifyContent: "center", alignItems: "center", overflow: "hidden" }}
      >
        <div
          className="pdf-viewer__container__document"
          ref={setContainerRef}
          style={{ width: "100%", height: "100%", display: "flex", justifyContent: "center", alignItems: "center", overflow: "hidden" }}
        >
          {pdfStatus === "succeeded" && pdfUrl && (
            <Stack justifyContent="center" alignItems="center" style={{ width: "100%", height: "100%", overflow: "auto" }}>
              {contentType?.includes("image/") ? (
                <img
                  src={pdfUrl ?? undefined}
                  alt="file"
                  style={{ maxWidth: "100%", maxHeight: "100%", height: "auto", objectFit: "contain" }}
                />
              ) : (
                <Document
                  file={pdfUrl}
                  onLoadSuccess={onDocumentLoadSuccess}
                  options={options}
                >
                  <Page
                    pageNumber={page}
                    width={containerRef ? containerRef.offsetWidth * scale : undefined}
                    height={containerRef ? containerRef.offsetHeight * scale : undefined}
                    renderMode="canvas"
                  />
                </Document>
              )}
              <Stack
                direction="row"
                justifyContent="space-around"
                alignItems="center"
                sx={{ width: "100%", marginTop: "10px" }}
              >
                <ButtonGroup aria-label="zoom button group">
                  <IconButton
                    onClick={handleZoomIn}
                    disabled={scale >= 2}
                    color="inherit"
                    aria-label="zoom in button"
                  >
                    <ZoomInIcon />
                  </IconButton>
                  <IconButton
                    onClick={handleZoomOut}
                    disabled={scale <= 0.5}
                    color="inherit"
                    aria-label="zoom out button"
                  >
                    <ZoomOutIcon />
                  </IconButton>
                </ButtonGroup>
                <Pagination
                  count={numPages}
                  page={page}
                  sx={{ color: "inherit" }}
                  shape="rounded"
                  onChange={handleChange}
                />
              </Stack>
            </Stack>
          )}
          {pdfStatus === "loading" && <Loading />}
          {pdfStatus === "failed" && (
            <Typography variant="h5">Error: {pdfError}</Typography>
          )}
        </div>
      </div>
    </div>
  );
}

export default PDFView;
