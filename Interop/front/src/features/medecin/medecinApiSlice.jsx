import {createEntityAdapter, createSelector} from "@reduxjs/toolkit";
import {apiSlice} from '../../app/api/apiSlice.jsx'

const medecinAdapter = createEntityAdapter({})
const initialState = medecinAdapter.getInitialState()


export const medecinApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getMedecins: builder.query({
            query: () => '/medecins',
            validateStatus: (response, result) => {
                return response.status === 200 && !result.isError
            },
            transformResponse: responseData => {
                console.log('transformResponse', responseData)
                return medecinAdapter.setAll(initialState, responseData)
            },
            providesTags: (result, error, arg) => {
                if (result?.ids) {
                    return [
                        {type: 'Medecin', id: 'List'},
                        ...result.ids.map(id => ({type: 'Medecin', id}))
                    ]
                } else return [{type: 'Medecin', id: 'LIST'}]
            },
            refetchOnMountOrArgChange: true,
        }),
        addNewMedecin: builder.mutation({
            query: initialMedecinData => ({
                url: '/medecins',
                method: 'POST',
                body: {
                    ...initialMedecinData,
                }
            }),
            invalidatesTags: [
                {type: 'Medecin', id: "LIST"}
            ]
        }),
        updateMedecin: builder.mutation({
            query: initialMedecinData => ({
                url: '/medecins',
                method: 'PATCH',
                body: {
                    ...initialMedecinData,
                }
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'Medecin', id: arg.id}
            ]
        }),
        deleteMedecin: builder.mutation({
            query: ({id}) => ({
                url: `/medecins`,
                method: 'DELETE',
                body: {
                    id
                }
            }),
            invalidatesTags: (result, error, arg) => [
                {type: 'Medecin', id: arg.id}
            ]
        })
    })
})

export const {
    useGetMedecinsQuery,
    useAddNewMedecinMutation,
    useUpdateMedecinMutation,
    useDeleteMedecinMutation
} = medecinApiSlice

// returns the query result object
export const selectMedecinsResult = medecinApiSlice.endpoints.getMedecins.select()

// creates memorized selector

const selectmedecinData = createSelector(
    selectMedecinsResult,
    medecinResult => medecinResult.data
)

// getSelectors creates these selectors and we rename them with aliases using destructuring
export const {
    selectAll: selectAllMedecins,
    selectById: selectMedecinById,
    selectIds: selectMedecinIds
} = medecinAdapter.getSelectors(state => selectmedecinData(state) ?? initialState)