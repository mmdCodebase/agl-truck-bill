import {
    createSlice,
    createAsyncThunk,
    AsyncThunk,
    PayloadAction,
} from "@reduxjs/toolkit";
import axios from "axios";
import type {
    AccruedCharge,
    ChargeSliceState,
} from "./types";

export const fetchAccruedCharges: AsyncThunk<AccruedCharge[], string, {}> =
    createAsyncThunk("accruedCharges/fetchAccruedCharges", async (shipmentNumber, { rejectWithValue }) => {
        try {
            // console.log("shipmentNumber: ", shipmentNumber)
            const response = await axios.get(
                `/wise/V1/UniversalXML/UniversalShipment/${shipmentNumber}/charges`
              );
            // console.log("charge======>",response.data)
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || error.message);
        }
    });

const initialState: ChargeSliceState = {
    charge: [],
    chargeStatus: "idle",
    chargeError: null,
};

const chargeSlice = createSlice({
    name: "charge",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchAccruedCharges.pending, (state) => {
                state.chargeStatus = "loading";
            })
            .addCase(
                fetchAccruedCharges.fulfilled,
                (state, action: PayloadAction<AccruedCharge[]>) => {
                    state.chargeStatus = "succeeded";
                    state.charge = action.payload;
                }
            )
            .addCase(fetchAccruedCharges.rejected, (state, action) => {
                state.chargeStatus = "failed";
                state.chargeError = action.payload as string;
            });
    },
});

export default chargeSlice.reducer;
