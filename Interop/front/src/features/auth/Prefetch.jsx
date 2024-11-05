import React from 'react'
import { store } from '../../app/store.jsx'
import { usersApiSlice } from '../users/usersApiSlice.jsx'
import { patientsApiSlice } from '../patients/patientsApiSlice.jsx'
import { useEffect } from 'react'
import { Outlet } from 'react-router-dom'

const Prefetch = () => {

    useEffect(() => {
        console.log('subscribing')
        const patients = store.dispatch(patientsApiSlice.endpoints.getpatients.initiate())
        const users = store.dispatch(usersApiSlice.endpoints.getusers.initiate())
        const medecins = store.dispatch(usersApiSlice.endpoints.getMedecins.initiate())

        return () => {
            console.log('unsubscribing')
            patients.unsubscribe()
            users.unsubscribe()
            medecins.unsubscribe()
        }
    },[])

    return <Outlet />
}

export default Prefetch









