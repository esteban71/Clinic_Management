import {createEntityAdapter, createSelector} from "@reduxjs/toolkit";
import {apiSlice} from '../../app/api/apiSlice.jsx'

const patientsAdapter = createEntityAdapter({})
const initialState = patientsAdapter.getInitialState()

export const patientsApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getpatients: builder.query({
            query: () => '/patients',
            validateStatus: (response, result) => {
                return response.status === 200 && !result.isError
            },
            transformResponse: responseData => {
                return patientsAdapter.setAll(initialState, responseData)
            },
            providesTags: (result, error, arg) => {
                if (result?.ids) {
                    return [
                        {type: 'Patient', id: 'List'},
                        ...result.ids.map(id => ({ type: 'Patient', id }))
                    ]
                } else return [{ type: 'Patient', id: 'LIST' }]
            },
            refetchOnMountOrArgChange: true,
        }),
        addNewPatient: builder.mutation({
            query: initialNote => ({
                url: '/patients',
                method: 'POST',
                body: {
                    ...initialNote,
                }
            }),
            invalidatesTags: [
                { type: 'Patient', id: "LIST" }
            ]
        }),
        updatePatient: builder.mutation({
            query: initialNote => ({
                url: '/patients',
                method: 'PATCH',
                body: {
                    ...initialNote,
                }
            }),
            invalidatesTags: (result, error, arg) => [
                { type: 'Patient', id: arg.id }
            ]
        }),
        deletePatient: builder.mutation({
            query: ({ id }) => ({
                url: `/patients`,
                method: 'DELETE',
                body: { id }
            }),
            invalidatesTags: (result, error, arg) => [
                { type: 'Patient', id: arg.id }
            ]
        }),
        
    })
})


export const {
    useGetpatientsQuery,
    useAddNewPatientMutation,
    useUpdatePatientMutation,
    useDeletePatientMutation
} = patientsApiSlice


// returns the query result object
export const selectpatientsResult = patientsApiSlice.endpoints.getpatients.select()


// creates memorized selector
const selectpatientsData = createSelector(
    selectpatientsResult,
    patientResult => patientResult.data
)


// getSelectors creates these selectors and we rename them with aliases using destructuring
export const {
    selectAll: selectAllPatients,
    selectById: selectPatientById,
    selectIds: selectPatientIds
} = patientsAdapter.getSelectors(state => selectpatientsData(state) ?? initialState)


