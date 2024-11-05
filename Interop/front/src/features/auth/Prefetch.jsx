import React, {useEffect} from 'react'
import {store} from '../../app/store.jsx'
import {usersApiSlice} from '../users/usersApiSlice.jsx'
import {patientsApiSlice} from '../patients/patientsApiSlice.jsx'
import {medecinApiSlice} from '../medecin/medecinApiSlice.jsx'
import {cabinetApiSlice} from '../cabinet/cabinetApiSlice.jsx'
import {Outlet} from 'react-router-dom'

const Prefetch = () => {

    useEffect(() => {
        console.log('subscribing')
        const patients = store.dispatch(patientsApiSlice.endpoints.getpatients.initiate())
        const users = store.dispatch(usersApiSlice.endpoints.getusers.initiate())
        const medecins = store.dispatch(medecinApiSlice.endpoints.getMedecins.initiate())
        const cabinet = store.dispatch(cabinetApiSlice.endpoints.getCabinets.initiate())

        return () => {
            console.log('unsubscribing')
            patients.unsubscribe()
            users.unsubscribe()
            medecins.unsubscribe()
            cabinet.unsubscribe()
        }
    },[])

    return <Outlet />
}

export default Prefetch









