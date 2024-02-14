import React from 'react';

function Footer() {
  return (
    <footer className="bg-indigo-600 text-white static bottom-0 w-full">
      <div className="">
        <div className="grid grid-cols-2 gap-6 items-center">
          {/* Privacy Policy */}
          <div className='text-center'>
              <h2 className="text-md sm:text-lg font-semibold text-gray-200 uppercase ">Legal</h2>
              <ul className="text-xs sm:text-sm text-gray-300">
                <li className="">
                <a className="hover:text-white" href="/privacy-policy">Privacy Policy</a>
                </li>
                <li>
                <a className="hover:text-white" href="/terms-of-service/">Terms of Use</a>
                </li>
              </ul>
            </div>

          {/* Contact Info */}

          <div className='text-center'>
              <h2 className="text-md sm:text-lg font-semibold text-gray-200 uppercase ">Contact Info</h2>
              <ul className="text-xs sm:text-sm text-gray-300">
              <li>
                <a className="hover:text-white" href="/about/">About</a>
                </li>
                <li className="">
                theedgepredictor@gmail.com
                </li>
      
              </ul>
            </div>

        </div>

        <hr className="my-2 border-gray-200 " />
        <div className="grid grid-cols-1 px-2 sm:grid-cols-2 sm:pb-0">

      {/* Social Media Links */}
    <div className="text-center text-sm space-x-4 pb-1 sm:text-right sm:order-2 sm:pr-2 sm:text-md text-gray-400  ">
      <a href="https://x.com/jb2bets" target="_blank" rel="noopener noreferrer">
        <i className="fab fa-twitter social-icon twitter-icon hover:text-white"></i>
      </a>
      <a href="https://medium.com/@TheEdgePredictor-" target="_blank" rel="noopener noreferrer">
        <i className="fab fa-medium social-icon medium-icon hover:text-white"></i>
      </a>
      <a href="https://discord.gg/UK5dThHku" target="_blank" rel="noopener noreferrer">
        <i className="fab fa-discord social-icon discord-icon hover:text-white"></i>
      </a>
      <a href="https://www.patreon.com/TheEdgePredictor" target="_blank" rel="noopener noreferrer">
        <i className="fab fa-patreon social-icon patreon-icon hover:text-white"></i>
      </a>
    </div>
          {/* Copyright */}
          <div className="text-center text-xs pb-1 sm:text-left sm:order-1 sm:text-sm sm:pl-2 text-gray-400">
          <p>&copy; {new Date().getFullYear()} The Edge Predictor. All rights reserved.</p>
        </div>

      

  </div>
  </div>
    </footer>
  );
}

export default Footer;