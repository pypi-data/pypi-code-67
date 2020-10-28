'''
 StaticRoute Genie Ops Object Outputs for NXOS.
'''

class StaticRouteOutput(object):
    # 'show ipv4 static route' output

    showIpv4StaticRoute = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.1.3.1',
                                            'next_hop_netmask': '32',
                                            'outgoing_interface': 'Ethernet1/2',
                                        },
                                    },
                                },
                            },
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.2.3.2',
                                            'next_hop_netmask': '32',
                                            'outgoing_interface': 'Ethernet1/4',
                                        },
                                        2: {
                                            'index': 2,
                                            'active': True,
                                            'next_hop': '10.229.3.2',
                                            'next_hop_netmask': '32',
                                            'outgoing_interface': 'Ethernet1/1',
                                        },
                                    },
                                },
                            },
                        },
                    },

                },
            },
        },

    }
    showIpv6StaticRoute = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'default',
                                            'rnh_active': False,
                                            'next_hop': '2001:10:1:3::1',
                                            'next_hop_netmask': '128',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'default',
                                            'rnh_active': False,
                                            'next_hop': '2001:20:1:3::1',
                                            'next_hop_netmask': '128',
                                            'outgoing_interface': 'Ethernet1/3',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'default',
                                            'rnh_active': False,
                                            'next_hop': '2001:10:2:3::2',
                                            'next_hop_netmask': '128',
                                            'outgoing_interface': 'Ethernet1/4',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'default',
                                            'rnh_active': False,
                                            'next_hop': '2001:20:2:3::2',
                                            'next_hop_netmask': '128',
                                            'outgoing_interface': 'Ethernet1/1',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'VRF1': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'outgoing_interface': 'Null0',
                                            'preference': 1,
                                            'resolved_tid': 80000003,
                                            'bfd_enabled': False,
                                            'rnh_active': False,
                                            'next_hop_vrf': 'VRF1',
                                        },
                                    },
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'VRF1',
                                            'rnh_active': False,
                                            'next_hop': '2001:10:1:3::1',
                                            'next_hop_netmask': '128',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'VRF1',
                                            'rnh_active': False,
                                            'next_hop': '2001:20:1:3::1',
                                            'next_hop_netmask': '128',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'outgoing_interface': 'Null0',
                                            'preference': 2,
                                            'resolved_tid': 80000003,
                                            'bfd_enabled': False,
                                            'rnh_active': False,
                                            'next_hop_vrf': 'VRF1',
                                        },
                                    },
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'VRF1',
                                            'rnh_active': False,
                                            'next_hop': '2001:10:2:3::2',
                                            'next_hop_netmask': '128',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'VRF1',
                                            'rnh_active': False,
                                            'next_hop': '2001:20:2:3::2',
                                            'next_hop_netmask': '128',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 1,
                                        },
                                        3: {
                                            'index': 3,
                                            'next_hop_vrf': 'VRF1',
                                            'rnh_active': True,
                                            'next_hop': '2001:20:2:3::2',
                                            'next_hop_netmask': '128',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 3,
                                        },
                                        4: {
                                            'index': 4,
                                            'next_hop_vrf': 'VRF1',
                                            'rnh_active': True,
                                            'next_hop': '2001:50:2:3::2',
                                            'next_hop_netmask': '128',
                                            'bfd_enabled': False,
                                            'resolved_tid': 0,
                                            'preference': 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },

    }

    staticRouteOpsOutput = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.1.3.1',
                                            'outgoing_interface': 'Ethernet1/2',
                                        },
                                    },
                                },
                            },
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.2.3.2',
                                            'outgoing_interface': 'Ethernet1/4',
                                        },
                                        2: {
                                            'index': 2,
                                            'active': True,
                                            'next_hop': '10.229.3.2',
                                            'outgoing_interface': 'Ethernet1/1',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'default',
                                            'next_hop': '2001:10:1:3::1',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'default',
                                            'next_hop': '2001:20:1:3::1',
                                            'outgoing_interface': 'Ethernet1/3',
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'default',
                                            'next_hop': '2001:10:2:3::2',
                                            'outgoing_interface': 'Ethernet1/4',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'default',
                                            'next_hop': '2001:20:2:3::2',
                                            'outgoing_interface': 'Ethernet1/1',
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'VRF1': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'outgoing_interface': 'Null0',
                                            'preference': 1,
                                            'next_hop_vrf': 'VRF1',
                                        },
                                    },
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'VRF1',
                                            'next_hop': '2001:10:1:3::1',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'VRF1',
                                            'next_hop': '2001:20:1:3::1',
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'outgoing_interface': 'Null0',
                                            'preference': 2,
                                            'next_hop_vrf': 'VRF1',
                                        },
                                    },
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop_vrf': 'VRF1',
                                            'next_hop': '2001:10:2:3::2',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop_vrf': 'VRF1',
                                            'next_hop': '2001:20:2:3::2',
                                            'preference': 1,
                                        },
                                        3: {
                                            'index': 3,
                                            'next_hop_vrf': 'VRF1',
                                            'next_hop': '2001:20:2:3::2',
                                            'preference': 3,
                                        },
                                        4: {
                                            'index': 4,
                                            'next_hop_vrf': 'VRF1',
                                            'next_hop': '2001:50:2:3::2',
                                            'preference': 5,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
