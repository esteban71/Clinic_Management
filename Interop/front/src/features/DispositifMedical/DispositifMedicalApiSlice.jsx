import {createEntityAdapter} from "@reduxjs/toolkit";
import {apiSlice} from '../../app/api/apiSlice';

const DispositifMedicalAdapter = createEntityAdapter({});
const initialState = DispositifMedicalAdapter.getInitialState();

export const DispositifMedicalApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getDispositifMedical: builder.query({
            query: (patientID) => `/dispositifs/${patientID}/dispositifs`,
            validateStatus: (response, result) => {
                return response.status === 200 && !result.isError
            },
            transformResponse: responseData => {
                return DispositifMedicalAdapter.setAll(initialState, responseData)
            },
            providesTags: (result, error, arg) => {
                if (result?.ids) {
                    return [
                        {type: 'MedicalReport', id: 'LIST'},
                        ...result.ids.map(id => ({type: 'MedicalReport', id}))
                    ];
                } else return [{type: 'DispositifMedical', id: 'LIST'}];
            },
            refetchOnMountOrArgChange: true,
        }),
        addNewDispositifMedical: builder.mutation({
            query: (report) => ({
                url: `/dispositifs/${report.patient_id}/new`,
                method: 'POST',
                body: report
            }),
            invalidatesTags: [{type: 'DispositifMedical', id: 'LIST'}]
        }),
        updateDispositifMedical: builder.mutation({
            query: (report) => ({
                url: `/dispositifs/${report.patient_id}/dispositif/${report.report_id}`,
                method: 'PATCH',
                body: report
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'DispositifMedical', id: arg.report_id}
            ]
        }),
        deleteDispositifMedical: builder.mutation({
            query: (report) => ({
                url: `/dispositifs/${report.patient_id}/dispositif/${report.report_id}`,
                method: 'DELETE'
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'DispositifMedical', id: arg.report_id}
            ]
        })
    })
});

export const {
    useGetDispositifMedicalQuery,
    useAddNewDispositifMedicalMutation,
    useUpdateDispositifMedicalMutation,
    useDeleteDispositifMedicalMutation
} = DispositifMedicalApiSlice;

