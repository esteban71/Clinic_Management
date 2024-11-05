import { configureStore } from "@reduxjs/toolkit";
import { apiSlice } from "./api/apiSlice.jsx";
import { setupListeners } from "@reduxjs/toolkit/dist/query";
import authReducer from '../features/auth/authSlice.jsx'

export const store = configureStore({
    reducer: {
        [apiSlice.reducerPath]: apiSlice.reducer,
        auth: authReducer,
    },
    middleware: getDefaultMiddleware => 
        getDefaultMiddleware().concat(apiSlice.middleware),
    devTools: false
})

setupListeners(store.dispatch)
