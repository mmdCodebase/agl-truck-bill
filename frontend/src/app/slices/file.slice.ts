import {
  createSlice,
  createAsyncThunk,
  AsyncThunk,
  PayloadAction,
} from "@reduxjs/toolkit";
import axios from "axios";
import { saveAs } from "file-saver";
import type { FileSliceState, FileResponse, CWUploadResponse } from "./types";
import { RootState } from "../store";

interface FetchFileArgs {
  attachmentId: string;
  filename: string;
  emailId: string;
}

export const fetchFile: AsyncThunk<FileResponse, FetchFileArgs, {}> = createAsyncThunk(
  "file/fetchFile",
  async ({ attachmentId, filename, emailId }: FetchFileArgs, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${process.env.API_URL}/V1/file`, {
        params: { attachment_id: attachmentId, file_name: filename, email_id: emailId },
        responseType: "blob",
      });
      // console.log("file=====>", response.data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || error.message);
    }
  }
);

export const downloadCWUpload: AsyncThunk<CWUploadResponse, void,{ state: RootState }> = createAsyncThunk(
  "file/downloadCWUpload",
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as RootState;
      const { cwUploadData } = state.data;
      const response = await axios.post(
        `${process.env.API_URL}/V1/file`,
        cwUploadData,
        {
          responseType: "blob",
        }
      );

      const contentDisposition = response.headers["content-disposition"];
      let filename = "CW1_NewChargeRate_Upsert.xlsx"; // Default filename
      if (contentDisposition) {
        const matches = /filename=([^;]+)/.exec(contentDisposition);
        if (matches != null && matches[1]) {
          filename = matches[1].trim();
        }
      }

      // Download CW data
      saveAs(response.data, filename);

      return { blob: response.data, filename };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || error.message);
    }
  }
);

const initialState: FileSliceState = {
  pdfBlob: null,
  pdfStatus: "idle",
  pdfError: null,
  cwUpload: null,
  downloadCWStatus: "idle",
  downloadCWError: null
};

const fileSlice = createSlice({
  name: "file",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchFile.pending, (state) => {
        state.pdfStatus = "loading";
      })
      .addCase(
        fetchFile.fulfilled,
        (state, action: PayloadAction<FileResponse>) => {
          state.pdfStatus = "succeeded";
          state.pdfBlob = action.payload;
        }
      )
      .addCase(fetchFile.rejected, (state, action) => {
        state.pdfStatus = "failed";
        state.pdfError = action.payload as string;
      })
      .addCase(downloadCWUpload.pending, (state) => {
        state.downloadCWStatus = "loading";
      })
      .addCase(
        downloadCWUpload.fulfilled,
        (state, action: PayloadAction<CWUploadResponse>) => {
          state.downloadCWStatus = "succeeded";
          state.cwUpload = action.payload;
        }
      )
      .addCase(downloadCWUpload.rejected, (state, action) => {
        state.downloadCWStatus = "failed";
        state.downloadCWError = action.payload as string;
      })
  },
});

export default fileSlice.reducer;
