import React from 'react'
import { useParams } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectPatientById } from './patientsApiSlice.jsx'
import { selectAllUsers } from '../users/usersApiSlice.jsx'
import EditPatientForm from './EditPatientForm'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'

const EditPatient = () => {

  const { id } = useParams()

  const patient = useSelector(state => selectPatientById(state, id))
  const users = useSelector(selectAllUsers)

  console.log('users', users)

  const content = users.length && patient ? <EditPatientForm patient={patient} users={users} /> : <CircularLoader />
  
  return content
}

export default EditPatient
