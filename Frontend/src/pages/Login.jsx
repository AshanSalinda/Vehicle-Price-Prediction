import React from 'react';
import logo from '../assets/logo.png';
import background from '../assets/background.jpeg';
import background1 from '../assets/background1.webp';
import background2 from '../assets/background2.jpg';
import Input from '../components/input';
import Button from '../components/input/Button';

function Login() {
  return (
    <div className='min-w-[100vw] min-h-[100vh] overflow-auto flex items-center justify-center'>
        <img src={background2} alt="background" className='absolute object-cover pointer-events-none w-full h-full brightness-[0.8]' />

        <div className='md:px-[5.2rem] w-full mx-3 md:w-fit py-11 bg-[#000000A0] backdrop-blur-sm rounded-xl shadow-[0_4px_30px_15px_#FFFFFF50] '>
            <h1 className='text-4xl font-semibold text-center text-white'>Login</h1>
            <form className='flex flex-col items-center w-[72vw] mx-auto mt-16 space-y-5 md:w-72'>
                <Input type='email' label="Email" />
                <Input type='password' label="Password" />
                <Button label='Login' sx={{width: "100%", marginTop: "1.5rem !important"}} />
            </form>
            <p className='mt-8 text-center cursor-pointer text-primary-500 hover:underline'>Forgot Password?</p>

            <img className='w-24 mx-auto mt-14' src={logo} alt="logo" />
        </div>
    </div>
  )
}

export default Login