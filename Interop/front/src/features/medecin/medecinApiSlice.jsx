import {createSelector, createEntityAdapter} from "@reduxjs/toolkit";
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
            }
        }),
    })
})

export const {
    useGetMedecinsQuery,
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