import {createEntityAdapter, createSelector} from "@reduxjs/toolkit";
import {apiSlice} from '../../app/api/apiSlice.jsx'

const cabinetAdapter = createEntityAdapter({})
const initialState = cabinetAdapter.getInitialState()


export const cabinetApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getCabinets: builder.query({
            query: () => '/cabinets',
            validateStatus: (response, result) => {
                return response.status === 200 && !result.isError
            },
            transformResponse: responseData => {
                return cabinetAdapter.setAll(initialState, responseData)
            },
            providesTags: (result, error, arg) => {
                if (result?.ids) {
                    return [
                        {type: 'Cabinet', id: 'List'},
                        ...result.ids.map(id => ({type: 'Cabinet', id}))
                    ]
                } else return [{type: 'Cabinet', id: 'LIST'}]
            }
        }),
    })
})

export const {
    useGetCabinetsQuery,
} = cabinetApiSlice


export const selectCabinerResult = cabinetApiSlice.endpoints.getCabinets.select()

const selectCabinetData = createSelector(
    selectCabinerResult,
    cabinetResult => cabinetResult.data
)

export const {
    selectAll: selectAllCabinets,
    selectById: selectCabinetById,
    selectIds: selectCabinetIds
} = cabinetAdapter.getSelectors(state => selectCabinetData(state) ?? initialState)