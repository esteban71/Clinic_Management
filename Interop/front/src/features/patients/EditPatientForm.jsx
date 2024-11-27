import React, {useEffect, useState} from 'react'
import {useDeletePatientMutation, useUpdatePatientMutation} from './patientsApiSlice.jsx'
import {useNavigate} from 'react-router-dom'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faSave, faTrashCan} from '@fortawesome/free-solid-svg-icons'
import InputAdornment from '@mui/material/InputAdornment';
import TextField from '@mui/material/TextField';
import useAuth from '../../hooks/useAuth.jsx'

const EMAIL_REGEX = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/
const MOBILENUMBER_REGEX = /^(\+\d{1,3}[- ]?)?\d{10}$/

const EditPatientForm = ({patient, medecin, cabinet}) => {

    const {isDoctor, username} = useAuth()

    const [
        updatePatient, {
            isLoading,
            isSuccess,
            isError,
            error
        }] = useUpdatePatientMutation()


    const [deletePatient, {
        isSuccess: isDelSuccess,
        isError: isDelError,
        error: delerror
    }] = useDeletePatientMutation()

    const navigate = useNavigate()

    const [name, setName] = useState(patient.name)
    const [email, setEmail] = useState(patient.email)
    const [validid, setvalidid] = useState(false)
    const [address, setAddress] = useState(patient.address)
    const [telecom, setTelecom] = useState(patient.telecom)
    const [validtelecom, setvalidtelecom] = useState(false)
    const [iserror, setIsError] = useState(false);
    const [cabinet_id, setCabinetId] = useState([patient.medecin.cabinet_medical_id]);
    const [medecin_id, setMedecin_id] = useState();

    useEffect(() => {
        setMedecin_id([patient.medecin.id]);
    }, [medecin, cabinet_id]);

    const onCabinetIdChanged = e => {
        const values = Array.from(
            e.target.selectedOptions,
            (option) => option.id
        )
        setCabinetId(values)
    }

    useEffect(() => {
        setvalidid(EMAIL_REGEX.test(email))
    }, [email])

    useEffect(() => {
        setvalidtelecom(MOBILENUMBER_REGEX.test(telecom))
    }, [telecom])


    useEffect(() => {

        if (isSuccess || isDelSuccess) {
            setName('')
            setAddress('')
            setTelecom('')
            setMedecin_id('')
            setCabinetId('')
            navigate('/dash/patients')
            window.location.reload()
        }

    }, [isSuccess, isDelSuccess, navigate])

    const onPatientNameChanged = e => setName(e.target.value)
    const onAddressChanged = e => setAddress(e.target.value)
    const onPatientPIDChanged = e => setEmail(e.target.value)
    const onMobileNumberChanged = e => setTelecom(e.target.value)
    const onDoctorIDChanged = e => {
        const values = Array.from(
            e.target.selectedOptions,
            (option) => option.id
        )
        console.log(values)
        setMedecin_id(values)
    }

    const canSave = [name, address, telecom, medecin_id].every(Boolean) && !isLoading

    const onSavePatientClicked = async (e) => {
        if (canSave && validid && validtelecom) {
            await updatePatient({
                'id': patient.id,
                'email': email,
                'name': name,
                'address': address,
                'telecom': telecom,
                'medecin_id': parseInt(medecin_id)
            })
            alert('Patient updated successfully')
        } else if (!validtelecom && !validid) {
            alert('Invalid Email ID and mobile number')
        } else if (!validtelecom) {
            alert('Invalid Mobile Number')
        } else if (!validid) {
            alert('Invalid Email ID')
        } else {
            alert('Unable to update patient! please try again...')
        }
    }

    const onDeletePatientClicked = async () => {
        await deletePatient({'id': patient.id})
        alert('Patient data deleted successfully')
    }

    let filteredDoctors = medecin


    const options_cabinet = cabinet.map(cabinet => {
        return (
            <option
                key={cabinet.id}
                value={cabinet.id}
                id={cabinet.id}

            > {cabinet.name} </option>
        )
    });

    const options = filteredDoctors
        .filter(user => user.cabinet_medical_id === parseInt(cabinet_id[0]))
        .map(user => {
            return (
                <option
                    key={user.id}
                    value={user.id}
                    id={user.id}

                > {user.name} </option>
            )
        })


    const errClass = (isError || isDelError) ? "errmsg" : "offscreen"
    const errContent = (error?.data?.message || delerror?.data?.message) ?? ''

    const content = (
        <>
            <p className={errClass}>{errContent}</p>
            <div className='form-main'>
                <form className="form" onSubmit={e => e.preventDefault()}>
                    <div className="form__title-row">
                        <h2>{patient.name} [ Token = {patient.id}]</h2>
                        <div className="form__action-buttons">
                            <button
                                className="icon-button"
                                title="Save"
                                onClick={onSavePatientClicked}
                            >
                                <FontAwesomeIcon icon={faSave}/>
                            </button>
                            <button
                                className="icon-button"
                                title="Delete"
                                onClick={onDeletePatientClicked}
                            >
                                <FontAwesomeIcon icon={faTrashCan}/>
                            </button>
                        </div>
                    </div>


                    <div className="patient-details-first-row">
                        <div className='patient-details-first-row--first-column'>
                            <div><TextField
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="text"
                                label="Enter Patient Name"
                                autoComplete="on"
                                value={name}
                                onChange={onPatientNameChanged}
                            /></div>


                            <div><TextField
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="text"
                                label="Enter Patient Address"
                                autoComplete="on"
                                value={address}
                                onChange={onAddressChanged}
                            /></div>


                            <div><TextField
                                required
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="tel"
                                label="Enter Patient Mobile Number"
                                autoComplete="on"
                                error={iserror}
                                value={telecom}
                                onChange={onMobileNumberChanged}
                                InputProps={{
                                    startAdornment: <InputAdornment position="start">
                                        +33
                                    </InputAdornment>,
                                }}
                            /></div>
                        </div>

                        <div className='patient-details-first-row--second-column'>

                            <div><TextField
                                className='form__input--patient'
                                id="note-title"
                                name="title"
                                type="text"
                                label="Enter Email ID"
                                autoComplete="off"
                                value={email}
                                onChange={onPatientPIDChanged}
                            /></div>

                            <div className="form__row">
                                <div className="form__divider">
                                    <label className="form__label form__checkbox-container" htmlFor="note-username">
                                        ASSIGNED TO CABINET:</label>
                                    <select
                                        id="note-username"
                                        name="username"
                                        className="form__select"
                                        value={cabinet_id}
                                        onChange={onCabinetIdChanged}
                                    >
                                        {options_cabinet}
                                    </select>
                                </div>
                            </div>

                            <div className="form__row">
                                <div className="form__divider">
                                    <label className="form__label form__checkbox-container" htmlFor="note-username">
                                        ASSIGNED TO DOCTOR:</label>
                                    <select
                                        id="note-username"
                                        name="username"
                                        className="form__select"
                                        value={medecin_id}
                                        onChange={onDoctorIDChanged}
                                    >
                                        {options}
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                </form>
            </div>
        </>
    )

    return content
}

export default EditPatientForm
