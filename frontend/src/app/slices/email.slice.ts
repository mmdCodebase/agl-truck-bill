import {
  createSlice,
  createAsyncThunk,
  AsyncThunk,
  PayloadAction,
} from "@reduxjs/toolkit";
import axios from "axios";
import type { EmailSliceState, FetchEmailsResponse} from "./types";

export const fetchEmails: AsyncThunk<FetchEmailsResponse, void, {}> =
  createAsyncThunk("email/fetchEmails", async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${process.env.API_URL}/V1/Emails`, {
        params: { email_status_id: 4 },
      });
      console.log("emails======>",response)
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || error.message);
    }
  });

const initialState: EmailSliceState = {
  emails: [],
  status: "idle",
  error: null,
  emailIndex: 0,
  attachmentIndex:0,
};

const emailSlice = createSlice({
  name: "email",
  initialState,
  reducers: {
    setEmailIndex: (state, action: PayloadAction<number>) => {
      state.emailIndex = action.payload;
    },
    setAttachmentIndex: (state, action: PayloadAction<number>) => {
      state.attachmentIndex = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchEmails.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(
        fetchEmails.fulfilled,
        (state, action: PayloadAction<FetchEmailsResponse>) => {
          state.status = "succeeded";
          state.emails = action.payload;
        }
      )
      .addCase(fetchEmails.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload as string;
      });
  },
});

export const { setEmailIndex, setAttachmentIndex } = emailSlice.actions;
export default emailSlice.reducer;