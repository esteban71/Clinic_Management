import {createEntityAdapter, createSelector} from "@reduxjs/toolkit";
import {apiSlice} from '../../app/api/apiSlice';

const medicalReportAdapter = createEntityAdapter({});
const initialState = medicalReportAdapter.getInitialState();

export const medicalReportApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getMedicalReports: builder.query({
            query: (patientID) => `/dossier/${patientID}/reports`,
            validateStatus: (response, result) => {
                return response.status === 200 && !result.isError
            },
            transformResponse: responseData => {
                return medicalReportAdapter.setAll(initialState, responseData)
            },
            providesTags: (result, error, arg) => {
                if (result?.ids) {
                    return [
                        {type: 'MedicalReport', id: 'LIST'},
                        ...result.ids.map(id => ({type: 'MedicalReport', id}))
                    ];
                } else return [{type: 'MedicalReport', id: 'LIST'}];
            },
            refetchOnMountOrArgChange: true,
        }),
        addNewMedicalReport: builder.mutation({
            query: (report) => ({
                url: `/dossier/${report.patient_id}/reports/new`,
                method: 'POST',
                body: report
            }),
            invalidatesTags: [{type: 'MedicalReport', id: 'LIST'}]
        }),
        updateMedicalReport: builder.mutation({
            query: ({patientID, report_id, ...updatedReport}) => ({
                url: `/dossier/${patientID}/reports/${report_id}`,
                method: 'PATCH',
                body: updatedReport
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'MedicalReport', id: arg.report_id}
            ]
        }),
        deleteMedicalReport: builder.mutation({
            query: ({patient_id, report_id}) => ({
                url: `/dossier/${patient_id}/reports/${report_id}`,
                method: 'DELETE'
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'MedicalReport', id: arg.report_id}
            ]
        })
    })
});

export const {
    useGetMedicalReportsQuery,
    useAddNewMedicalReportMutation,
    useUpdateMedicalReportMutation,
    useDeleteMedicalReportMutation
} = medicalReportApiSlice;

// returns the query result object
export const selectMedicalReportsResult = medicalReportApiSlice.endpoints.getMedicalReports.select();


// creates memorized selector
const selectMedicalReportData = createSelector(
    selectMedicalReportsResult,
    medicalReportsResult => medicalReportsResult.data
);

// getSelectors creates these selectors and we rename them with aliases using destructuring
export const {
    selectAll: selectAllMedicalReports,
    selectById: selectMedicalReportById,
    selectIds: selectMedicalReportIds
} = medicalReportAdapter.getSelectors(state => selectMedicalReportData(state) ?? initialState);
