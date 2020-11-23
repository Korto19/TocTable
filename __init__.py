# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TocTable
                                 A QGIS plugin
 TocTable
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-11-23
        copyright            : (C) 2020 by Giulio Fattori
        email                : giulio.fattori@tin.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Giulio Fattori'
__date__ = '2020-11-23'
__copyright__ = '(C) 2020 by Giulio Fattori'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load TocTable class from file TocTable.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .TocTable import TocTablePlugin
    return TocTablePlugin()