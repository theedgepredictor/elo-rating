import React, { useEffect,useState } from 'react';
import { Dialog } from '@headlessui/react'
import { Bars3Icon, XMarkIcon, UserCircleIcon } from '@heroicons/react/24/outline'
import {SPORTS} from'../backend/consts.js'
import { Link } from "react-router-dom"
function NavBar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [isSubMenuVisible, setSubMenuVisibility] = useState(false);

  const handleSubMenuToggle = () => {
    setSubMenuVisibility(!isSubMenuVisible);
  };

  const navigation = [
    {
      id: 1,
      name: 'TEAM RATINGS',
      href: `/team`
    },
    {
      id: 2,
      name: 'UPCOMING EVENTS',
      href: `/events`
    },
    {
      id: 3,
      name: 'PAST EVENTS',
      href: `/past-events`
    }
  ]

  return (
    <header className="sticky top-0  z-50">
        <nav className="flex items-center justify-between p-6 lg:px-8 border-b-2" aria-label="Global">
          <div className="flex lg:flex-1">
            <Link to="/" className="-m-1.5 px-3 mr-2">
              <span className="sr-only">Elo Rating</span>
              <img
                className="h-8 w-auto"
                alt="Elo Rating"
                src={'../../imgs/logo-no-background.png'}
              />
            </Link>
          </div>
          <div className="flex lg:hidden">
            <button
              type="button"
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
              onClick={() => setMobileMenuOpen(true)}
            >
              <span className="sr-only">Open main menu</span>
              <Bars3Icon className="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <div className="hidden lg:flex lg:gap-x-12">
            {navigation.map((item) => (
              <Link key={item.name} to={item.href} className=" text-md font-semibold leading-6 text-gray-900 text-center">
                {item.name}
              </Link>
            ))}
              <Link key={'ABOUT'} to={'/about'} className=" text-md font-semibold leading-6 text-gray-900 text-center">
                ABOUT
              </Link>
          </div>

          <div className="hidden lg:flex lg:flex-1 lg:justify-end">
          <button
            className="text-md font-semibold leading-6 text-gray-900 focus:outline-none"
            onClick={handleSubMenuToggle}
          >
            <UserCircleIcon className="h-8 w-8 text-gray-700" aria-hidden="true" />
          </button>
    </div>


        </nav>
        <Dialog as="div" className="lg:hidden" open={mobileMenuOpen} onClose={setMobileMenuOpen}>
          <div className="fixed inset-0 z-50" />
          <Dialog.Panel className="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
            <div className="flex items-center justify-between">
              <Link to="/" className="-m-1.5 p-1.5">
                <span className="sr-only">Elo Rating</span>
                <img
                  className="h-8 w-auto"
                  src={'../../imgs/logo-no-background.png'}
                  alt="Elo Rating"
                />
              </Link>
              <button
                type="button"
                className="-m-2.5 rounded-md p-2.5 text-gray-700"
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="sr-only">Close menu</span>
                <XMarkIcon className="h-6 w-6" aria-hidden="true" />
              </button>
            </div>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/10">
                <div className="space-y-2 py-6">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                    >
                      {item.name}
                    </Link>
                  ))}
              <Link key={'ABOUT'} to={'/about'} className=" -mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                ABOUT
              </Link>
                </div>
                </div>
            </div>
          </Dialog.Panel>
        </Dialog>
      </header>
  );
};

export default NavBar;