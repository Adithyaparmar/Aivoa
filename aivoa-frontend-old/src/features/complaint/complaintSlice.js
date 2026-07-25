import { createSlice } from '@reduxjs/toolkit';

// Field set mirrors the reference "Log Customer Complaint" screenshot:
// origin/customer, product/batch identification, complaint details, initial assessment.
const initialFormState = {
  complaintSource: '',
  customerName: '',
  productName: '',
  productStrengthGrade: '',
  batchLotNumber: '',
  manufacturingDate: '',
  expiryDate: '',
  quantityAffected: '',
  complaintType: '',
  complaintDate: '',
  complaintDescription: '',
  initialSeverity: '',
  priority: '',
};

const initialState = {
  status: 'Pending Triage', // Pending Triage | Saved | Submitting | Error
  fields: initialFormState,
  saveError: null,
};

const complaintSlice = createSlice({
  name: 'complaint',
  initialState,
  reducers: {
    fieldChanged(state, action) {
      const { name, value } = action.payload;
      state.fields[name] = value;
    },
    // Bulk-populate from AI extraction results — only fills fields the
    // extractor actually returned, leaves the rest for manual entry.
    fieldsPopulated(state, action) {
      state.fields = { ...state.fields, ...action.payload };
    },
    formReset(state) {
      state.fields = initialFormState;
      state.status = 'Pending Triage';
      state.saveError = null;
    },
    saveStarted(state) {
      state.status = 'Submitting';
      state.saveError = null;
    },
    saveSucceeded(state) {
      state.status = 'Saved';
    },
    saveFailed(state, action) {
      state.status = 'Error';
      state.saveError = action.payload;
    },
  },
});

export const {
  fieldChanged,
  fieldsPopulated,
  formReset,
  saveStarted,
  saveSucceeded,
  saveFailed,
} = complaintSlice.actions;

export default complaintSlice.reducer;
