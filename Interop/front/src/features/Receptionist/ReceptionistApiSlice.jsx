import {createEntityAdapter, createSelector} from "@reduxjs/toolkit";
import {apiSlice} from '../../app/api/apiSlice.jsx'

const ReceptionistAdapter = createEntityAdapter({})
const initialState = ReceptionistAdapter.getInitialState()


export const receptionistApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getReceptionists: builder.query({
            query: () => '/receptionists',
            validateStatus: (response, result) => {
                return response.status === 200 && !result.isError
            },
            transformResponse: responseData => {
                console.log('transformResponse', responseData)
                return ReceptionistAdapter.setAll(initialState, responseData);
            },
            providesTags: (result, error, arg) => {
                if (result?.ids) {
                    return [
                        {type: 'Receptionist', id: 'LIST'},
                        ...result.ids.map(id => ({type: 'Receptionist', id}))
                    ]
                } else return [{type: 'Receptionist', id: 'LIST'}]
            },
            refetchOnMountOrArgChange: true,
        }),
        addNewReceptionist: builder.mutation({
            query: initialMedecinData => ({
                url: '/receptionists',
                method: 'POST',
                body: {
                    ...initialMedecinData,
                }
            }),
            invalidatesTags: [
                {type: 'Medecin', id: "LIST"}
            ]
        }),
        updateReceptionist: builder.mutation({
            query: initialMedecinData => ({
                url: '/receptionists',
                method: 'PATCH',
                body: {
                    ...initialMedecinData,
                }
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'Receptionist', id: arg.id}
            ]
        }),
        deleteReceptionist: builder.mutation({
            query: ({id}) => ({
                url: `/receptionists`,
                method: 'DELETE',
                body: {
                    id
                }
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'Receptionist', id: arg.id}
            ]
        })
    })
})

export const {
    useGetReceptionistsQuery,
    useAddNewReceptionistMutation,
    useUpdateReceptionistMutation,
    useDeleteReceptionistMutation
} = receptionistApiSlice

// returns the query result object
export const selectReceptionistsResult = receptionistApiSlice.endpoints.getReceptionists.select()

// creates memorized selector

const selectReceptionistData = createSelector(
    selectReceptionistsResult,
    ReceptionistResult => ReceptionistResult.data
)

// getSelectors creates these selectors and we rename them with aliases using destructuring
export const {
    selectAll: selectAllReceptionists,
    selectById: selectReceptionistById,
    selectIds: selectReceptionistIds
} = ReceptionistAdapter.getSelectors(state => selectReceptionistData(state) ?? initialState)