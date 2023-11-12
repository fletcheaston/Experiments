"use client"

import { Menu, Transition } from "@headlessui/react"
import classNames from "classnames"
import Link from "next/link"
import React, { Fragment } from "react"

type LinkProps = Pick<React.ComponentProps<typeof Link>, "href" | "children">

export function Dropdown({ title, links }: { title: React.ReactNode; links: Array<LinkProps> }) {
    return (
        <div className="text-right">
            <Menu
                as="div"
                className="relative inline-block text-left"
            >
                {({ open }) => (
                    <>
                        <Menu.Button
                            className={classNames(
                                "btn btn-lg inline-flex w-full justify-center",
                                open ? "btn-primary" : "btn-primary-outline",
                            )}
                        >
                            {title}
                        </Menu.Button>

                        <Transition
                            as={Fragment}
                            show={open}
                            enter="transition ease-out duration-100"
                            enterFrom="transform opacity-0 scale-95"
                            enterTo="transform opacity-100 scale-100"
                            leave="transition ease-in duration-75"
                            leaveFrom="transform opacity-100 scale-100"
                            leaveTo="transform opacity-0 scale-95"
                        >
                            <Menu.Items className="absolute right-0 mt-2 w-fit origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-black/5 focus:outline-none">
                                {links.map((link) => {
                                    return (
                                        <Menu.Item key={link.href.toString()}>
                                            <div className="btn btn-secondary whitespace-nowrap px-0 text-left">
                                                <Link
                                                    href={link.href}
                                                    className=""
                                                >
                                                    <div className="w-full px-6">{link.children}</div>
                                                </Link>
                                            </div>
                                        </Menu.Item>
                                    )
                                })}
                            </Menu.Items>
                        </Transition>
                    </>
                )}
            </Menu>
        </div>
    )
}
