import React, {useEffect} from 'react'
import {Link, useLocation, useNavigate} from 'react-router-dom'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {
    faFileCirclePlus,
    faHouse,
    faRightFromBracket,
    faUserCircle,
    faUserPlus
} from '@fortawesome/free-solid-svg-icons'
import {useSendLogoutMutation} from '../features/auth/authApiSlice.jsx'
import useAuth from '../hooks/useAuth.jsx'

const DASH_REGEX = /^\/dash(\/)?$/
const PATIENTS_REGEX = /^\/dash\/patients(\/)?$/
const USERS_REGEX = /^\/dash\/users(\/)?$/

const DashHeader = () => {

    const { isDoctor } = useAuth()

    const navigate = useNavigate()
    const { pathname } = useLocation()

    const onGoHomeClicked = () => navigate('/dash')
    const onAddNewPatient = () => navigate('/dash/patients/new')
    const onAddNewUser = () => navigate('/dash/users/new')
    const onAddNewDoctor = () => navigate('/dash/medecins/new')

    let goHomeButton = null
    if(pathname !== '/dash') {
        goHomeButton = (
            <button
            className="dash-header__button icon-button"
            title="Home"
            onClick={onGoHomeClicked}
            >
                <FontAwesomeIcon icon={faHouse} style={{fontSize: 'large'}} />
            </button>
        )
    }

    let addNewPatient = null
    if(pathname === '/dash/patients' && !isDoctor) {
        addNewPatient = (
            <button
            className="dash-header__button icon-button"
            title="Add New Patient"
            onClick={onAddNewPatient}
            >
                <FontAwesomeIcon icon={faFileCirclePlus} style={{fontSize: 'large'}} />
            </button>
        )
    }

    let addNewUser = null
    if(pathname === '/dash/users' && !isDoctor) {
        addNewUser = (
            <button
            className="dash-header__button icon-button"
            title="Add New User"
            onClick={onAddNewUser}
            >
                <FontAwesomeIcon icon={faUserPlus} />
            </button>
        )
    }

    let addNewDoctor = null
    if (pathname === '/dash/medecins') {
        addNewDoctor = (
            <button
            className="dash-header__button icon-button"
            title="Add New Doctor"
            onClick={onAddNewDoctor}
            >
                <FontAwesomeIcon icon={faUserCircle} style={{fontSize: 'large', paddingTop: '0.1em'}} />
            </button>
        )
    }

    const [sendLogout, {
        isLoading,
        isSuccess,
        isError,
        error
    }] = useSendLogoutMutation()

    useEffect(() => {
        if(isSuccess) navigate('/')
    }, [isSuccess, navigate])

    if(isLoading) return (
        <span style={{ display: 'flex', justifyContent: 'center', marginTop: '2em' }}>
        <p>Logging out...</p>
        </span>
    )

    if(isError) return <p>Error: {error.data?.message}</p>

    let dashClass = null
    if(!DASH_REGEX.test(pathname) && !PATIENTS_REGEX.test(pathname) && !USERS_REGEX.test(pathname)) {
        dashClass = "dash-header__container--small"
    }
    
    const logoutButton = (
        <button 
        className='icon-button'
        title='Logout'
        onClick={sendLogout}>
            <FontAwesomeIcon icon={faRightFromBracket} style={{fontSize: 'large'}} />
        </button>
    )
    
    const content = (
        <header className="dash-header">
            <div className="dash-header__container">
                <Link to="/dash">
                    <h1 className="dash-header__title">Dashboard</h1>
                </Link>
                <nav className="dash-header__nav">
                    {/* add nav buttons later */}
                    {goHomeButton}
                    {addNewUser}
                    {addNewPatient}
                    {addNewDoctor}
                    {logoutButton}
                </nav>
            </div>
        </header>
    )
    
    return content

}

export default DashHeader