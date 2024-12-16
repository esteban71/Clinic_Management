import {createEntityAdapter} from "@reduxjs/toolkit";
import {apiSlice} from '../../app/api/apiSlice';

const ObservationAdapter = createEntityAdapter({});
const initialState = ObservationAdapter.getInitialState();

export const ObservationApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getObservation: builder.query({
            query: (patientID) => `/dispositifs/${patientID}/observations`,
            validateStatus: (response, result) => {
                return response.status === 200 && !result.isError
            },
            transformResponse: responseData => {
                return ObservationAdapter.setAll(initialState, responseData)
            },
            providesTags: (result, error, arg) => {
                if (result?.ids) {
                    return [
                        {type: 'MedicalReport', id: 'LIST'},
                        ...result.ids.map(id => ({type: 'MedicalReport', id}))
                    ];
                } else return [{type: 'Observation', id: 'LIST'}];
            },
            refetchOnMountOrArgChange: true,
        }),
        deleteObservation: builder.mutation({
            query: (report) => ({
                url: `/dispositifs/${report.patient_id}/observations/${report.report_id}`,
                method: 'DELETE'
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'Observation', id: arg.report_id}
            ]
        })
    })
});

export const {
    useGetObservationQuery,
    useDeleteObservationMutation,
} = ObservationApiSlice;