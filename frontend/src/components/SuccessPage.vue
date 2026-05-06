<template>
    <div class="min-h-screen p-5 bg-[#f7f7f7] flex justify-center items-center font-sans">
      <div class="bg-white rounded-xl p-10 text-center shadow-[0_2px_8px_rgba(0,0,0,0.08)]">
        <h1 class="text-[#4caf50] mt-0">Payment Successful!</h1>
        <p>Your order has been placed and sent to the dining hall.</p>
        <button class="bg-[#4caf50] text-white border-none rounded-[10px] px-5 py-3 font-semibold cursor-pointer mt-5" @click="$router.push('/')">
          Return Home
        </button>
      </div>
    </div>
  </template>
  