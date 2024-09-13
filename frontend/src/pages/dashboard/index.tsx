import { useState, useEffect } from "react";
import { Box, Divider, Grid, IconButton, Stack } from "@mui/material";
import { Close as CloseIcon } from "@mui/icons-material";
import { SnackbarKey, useSnackbar } from "notistack";
// components
import ExcelView from "./ExcelView";
import AttachmentView from "./AttachmentView";
import PDFView from "./PDFView";
import Sidebar from "./Sidebar";
import LinksView from "./LinksView";
// hooks
import { useAppDispatch, useAppSelector } from "@/app/hooks";
// reducer
import { fetchEmails, setEmailIndex, setAttachmentIndex } from "@/app/slices/email.slice";
import { downloadCWUpload, fetchFile } from "@/app/slices/file.slice";
import { fetchCWData, fetchData } from "@/app/slices/data.slice";
import { saveAction, skipAction } from "@/app/slices/action.slice";
import { FetchDataResponse } from "@/app/slices/types";

function Dashboard() {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const dispatch = useAppDispatch();
  const {
    emails,
    emailIndex,
    attachmentIndex,
    status: emailStatus,
    error: emailError,
  } = useAppSelector((state) => state.email);
  const { pdfBlob, pdfStatus, pdfError, downloadCWStatus, downloadCWError } =
    useAppSelector((state) => state.file);
  const pdfUrl = pdfBlob ? URL.createObjectURL(pdfBlob) : null;

  const {
    data,
    dataStatus,
    dataError,
    cwUploadData,
    cwUploadDataStatus,
    cwUploadDataError,
  } = useAppSelector((state) => state.data);

  const {
    skipActionStatus,
    skipActionError,
    saveActionStatus,
    saveActionError,
  } = useAppSelector((state) => state.action);


  // Get emails
  useEffect(() => {
    dispatch(fetchEmails());
    dispatch(fetchCWData("PENDING_CW_UPLOAD"));
  }, []);


  // Close alert icon
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

  // Showing emails status
  useEffect(() => {
    if (emailStatus === "succeeded") {
      enqueueSnackbar("Successfully loaded the email data.", {
        variant: "success",
      });
    } else if (emailStatus === "failed") {
      enqueueSnackbar(emailError, {
        variant: "error",
        persist: true,
        action: closeAction,
      });
    }
  }, [emailStatus]);

  // Showing file status
  useEffect(() => {
    if (pdfStatus === "succeeded") {
      enqueueSnackbar("Successfully loaded the TrukBill PDF file.", {
        variant: "success",
      });
    } else if (pdfStatus === "failed") {
      enqueueSnackbar(pdfError, {
        variant: "error",
        persist: true,
        action: closeAction,
      });
    }
  }, [pdfStatus]);

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

  // Showing data status
  useEffect(() => {
    if (dataStatus === "succeeded") {
      enqueueSnackbar("Successfully loaded the TruckBill data.", {
        variant: "success",
      });
    } else if (dataStatus === "failed") {
      enqueueSnackbar(dataError, {
        variant: "error",
        persist: true,
        action: closeAction,
      });
    }
  }, [dataStatus]);

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

  // Showing action status
  useEffect(() => {
    if (skipActionStatus === "succeeded") {
      enqueueSnackbar("Successfully skipped the CW Upload data.", {
        variant: "success",
      });
    } else if (skipActionStatus === "failed") {
      enqueueSnackbar(skipActionError, {
        variant: "error",
        persist: true,
        action: closeAction,
      });
    }
  }, [skipActionStatus]);

  useEffect(() => {
    if (saveActionStatus === "succeeded") {
      enqueueSnackbar("Successfully saved the CW Upload data.", {
        variant: "success",
      });
    } else if (saveActionStatus === "failed") {
      enqueueSnackbar(saveActionError, {
        variant: "error",
        persist: true,
        action: closeAction,
      });
    }
  }, [saveActionStatus]);

  // Get PDF file by filename
  useEffect(() => {
    if (!!emails.length) {
      const filename = emails[emailIndex].attachments[attachmentIndex].file_name;
      const emailId = emails[emailIndex].email_id;
      const attachmentId = emails[emailIndex].attachments[attachmentIndex].attachment_id;
      dispatch(fetchFile({ attachmentId, filename, emailId }));
      dispatch(fetchData({ attachmentId, emailId }));
    }
  }, [emails, emailIndex, attachmentIndex]);


  const changeEmailIndex = (newIndex: number) => {
    // Set email index
    if ((!!emails.length && newIndex >= 0) || newIndex < emails.length) {
      dispatch(setEmailIndex(newIndex));
      dispatch(setAttachmentIndex(0));
    }
  };

  const skipForManualReview = async () => {
    if (!!emails.length) {
      const email_id = emails[emailIndex].email_id;
      await dispatch(skipAction(email_id));
      changeEmailIndex(emailIndex + 1);
      dispatch(setAttachmentIndex(0));
    }
  };

  const saveForCWUpload = async (debit_note_data: FetchDataResponse) => {
    if (!!emails.length) {
      const email_id = emails[emailIndex].email_id;
      await dispatch(saveAction({ email_id, debit_note_data }));
      changeEmailIndex(emailIndex + 1);
      dispatch(setAttachmentIndex(0));
      await dispatch(fetchCWData("PENDING_CW_UPLOAD"));
    }
  };

  const downloadCWUploadTemplate = async () => {
    if (!!cwUploadData.length) {
      await dispatch(downloadCWUpload());
      await dispatch(fetchCWData("PENDING_CW_UPLOAD"));
    }
  };

  return (
    <Stack spacing={3} sx={{ position: 'relative' }}>
      <ExcelView
        cwData={cwUploadData}
        cwStatus={cwUploadDataStatus}
        downloadCWUploadTemplate={downloadCWUploadTemplate}
      />
      <Divider />
      <Box>
        <Grid container spacing={2}>
          <Grid item sm={8}>
            <AttachmentView
              attachmentData={emails[emailIndex]?.attachments?.flatMap((attachment) => attachment)}
              attachmentStatus={emailStatus}
            />
            <PDFView
              pdfUrl={pdfUrl}
              pdfStatus={pdfStatus}
              pdfError={pdfError}
              contentType={emails[emailIndex]?.attachments[attachmentIndex]?.content_type}
            />

          </Grid>
          <Grid item sm={4}>
            <Sidebar
              data={data}
              dataStatus={dataStatus}
              emails={emails}
              emailIndex={emailIndex}
              changeEmailIndex={changeEmailIndex}
              skipForManualReview={skipForManualReview}
              saveForCWUpload={saveForCWUpload}
            />
          </Grid>
        </Grid>
      </Box>
      <Divider />
      <LinksView />
    </Stack>
  );
}

export default Dashboard;
