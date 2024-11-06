import React from 'react'
import {useSelector} from 'react-redux'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import {selectAllCabinets} from "../cabinet/cabinetApiSlice.jsx";
import NewReceptionistForm from "./NewReceptionistForm.jsx";

const NewReceptionist = () => {

    const cabinet_data = useSelector(selectAllCabinets)

    const content = cabinet_data ? <NewReceptionistForm cabinet={cabinet_data}/> : <CircularLoader/>

    return content

}

export default NewReceptionist
