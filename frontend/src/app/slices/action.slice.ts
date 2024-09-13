import {
    createSlice,
    createAsyncThunk,
    AsyncThunk,
    PayloadAction,
  } from "@reduxjs/toolkit";
  import axios from "axios";
  import type {
    ActionSliceState,
    FetchDataResponse,
    ActionResponse,
  } from "./types";
  
  export const skipAction: AsyncThunk<ActionResponse, string, {}> =
    createAsyncThunk(
      "action/skipAction",
      async (email_id: string, { rejectWithValue }) => {
        try {
          const response = await axios.post(
            `${process.env.API_URL}/V1/actions`,
            {},
            {
              params: { email_id, action_type: "SKIPPED" },
            }
          );
          return response.data;
        } catch (error: any) {
          return rejectWithValue(error.response?.data?.detail || error.message);
        }
      }
    );
  
  export const saveAction: AsyncThunk<
    ActionResponse,
    { email_id: string; debit_note_data: FetchDataResponse },
    {}
  > = createAsyncThunk(
    "action/saveAction",
    async ({ email_id, debit_note_data }, { rejectWithValue }) => {
      try {
        const response = await axios.post(
          `${process.env.API_URL}/V1/actions`,
          debit_note_data,
          {
            params: { email_id, action_type: "PENDING_CW_UPLOAD" },
          }
        );
        return response.data;
      } catch (error: any) {
        return rejectWithValue(error.response?.data?.detail || error.message);
      }
    }
  );
  
  const initialState: ActionSliceState = {
    skipAction: null,
    skipActionStatus: "idle",
    skipActionError: null,
    saveAction: null,
    saveActionStatus: "idle",
    saveActionError: null,
  };
  
  const actionSlice = createSlice({
    name: "action",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
      builder
        .addCase(skipAction.pending, (state) => {
          state.skipActionStatus = "loading";
        })
        .addCase(
          skipAction.fulfilled,
          (state, action: PayloadAction<ActionResponse>) => {
            state.skipActionStatus = "succeeded";
            state.skipAction = action.payload;
          }
        )
        .addCase(skipAction.rejected, (state, action) => {
          state.skipActionStatus = "failed";
          state.skipActionError = action.payload as string;
        })
        .addCase(saveAction.pending, (state) => {
          state.saveActionStatus = "loading";
        })
        .addCase(
          saveAction.fulfilled,
          (state, action: PayloadAction<ActionResponse>) => {
            state.saveActionStatus = "succeeded";
            state.saveAction = action.payload;
          }
        )
        .addCase(saveAction.rejected, (state, action) => {
          state.saveActionStatus = "failed";
          state.saveActionError = action.payload as string;
        });
    },
  });
  
  export default actionSlice.reducer;
  