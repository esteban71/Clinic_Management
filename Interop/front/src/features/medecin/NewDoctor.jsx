import React from 'react'
import {useSelector} from 'react-redux'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import {selectAllCabinets} from "../cabinet/cabinetApiSlice.jsx";
import NewDoctorForm from "./NewDoctorForm.jsx";

const NewDoctor = () => {

    const cabinet_data = useSelector(selectAllCabinets)

    const content = cabinet_data ? <NewDoctorForm cabinet={cabinet_data}/> : <CircularLoader/>

    return content

}

export default NewDoctor
