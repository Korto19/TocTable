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
"""

__author__ = 'Giulio Fattori'
__date__ = '2020-11-23'
__copyright__ = '(C) 2020 by Giulio Fattori'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsProject,
					   QgsField,
					   QgsFields,
					   QgsFeature,
                       QgsFeatureSink,
					   QgsMapLayerType,
					   QgsWkbTypes,
					   QgsLayerTreeGroup,
					   QgsLayerTreeLayer,
					   QgsProcessingException,
                       QgsProcessingAlgorithm,
					   QgsProcessingParameterEnum,
					   QgsProcessingParameterField,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
import datetime

#questo per l'icona dell'algoritmo di processing
import os
import inspect
from qgis.PyQt.QtGui import QIcon

fields_list = ['Layer_N','Layer_Group_Level','Layer_Storage','Layer_Name','Geometry_Not_Valid','Layer_Crs','Layer_Type','Layer_Type_Name','Layer_Source','Raster_type','Raster_data_type','Raster_Info_dim','Raster_extent','Raster_Info_res','Raster_NoDataValue','Layer_Feature_Count','Layer_Meta_Parent_Id','Layer_Meta_Identifier','Layer_Meta_Title','Layer_Meta_Type','Layer_Meta_Language','Layer_Meta_Abstract']
default_fields = ','.join(str(e) for e in list(range(len(fields_list))))

class TocTableAlgorithm(QgsProcessingAlgorithm):
    """
    TOC algorithm retrieve info from Metadata and some 
	attributes of each layer and collect it's in a table.
    """
    INPUT_F = 'INPUT_F'
    OUTPUT = 'OUTPUT'


    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)
        
    #icona dell'algoritmo di processing
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icon.png')))
        return icon

    def createInstance(self):
        return TocTableAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Toc Table'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Toc Table')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return ''

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("The algorithm retrieves some properties and metadata of the project layers and \
                        inserts them in a table so that they can be inserted in the prints. Keeps track\
                        of the order of layers in the project and any groups\n \
                        Questo algoritmo recupera alcuni metadati e proprietà dei layer del progetto e\
                        li raccoglie in una tabella così da poterli inserire nelle stampe.\
                        Tiene traccia dell'ordine dei layer nel progetto e degli eventuali gruppi")
				

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
       
		# We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Project_Layers_Table ' + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
			 
            )
        )

        self.addParameter(
            #QgsProcessingParameterField(
            QgsProcessingParameterEnum(
                self.INPUT_F,
                self.tr('Campi da inserire nella TocTable'),
                #'Layer_N;Layer_Group_Level;Layer_Storage;Layer_Name;Geometry_Not_Valid;Layer_Crs;Layer_Type;Layer_Type_Name;Layer_Source;Raster_type;Raster_data_type;Raster_Info_dim;Raster_extent;Raster_Info_res;Raster_NoDataValue;Layer_Feature_Count;Layer_Meta_Parent_Id;Layer_Meta_Identifier;Layer_Meta_Title;Layer_Meta_Type;Layer_Meta_Language;Layer_Meta_Abstract',
                options = fields_list,
                defaultValue = default_fields,
                allowMultiple = True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        #i_fields = self.parameterAsMatrix(
        fields_enums = self.parameterAsEnums(
            parameters,
            self.INPUT_F,
            context)
        
        i_fields = [fields_list[i] for i in fields_enums]
		
        #CREA TABELLA CONTENUTI PROGETTO
        #per altri campi occorre vedere quali si serve aggiungere
        
        #funzione iterativa per posizione layer nella TOC
        def get_group_layers(group, level):
            level = level + group.name() + ' - '#' >> '
            for child in group.children():
                if isinstance(child, QgsLayerTreeGroup):
                    get_group_layers(child, level)
                else:
                    TOC_dict [child.name()] = level
                    #print(lev)
                    
        #dizionario delle posizioni
        TOC_dict ={}
        
        root = QgsProject.instance().layerTreeRoot()
        for child in root.children():
            level = 'root - ' #' >> '
            if isinstance(child, QgsLayerTreeGroup):
                get_group_layers(child, level)
            elif isinstance(child, QgsLayerTreeLayer):
                #lev = level #+ child.name())
                TOC_dict[child.name()] = level
        
        #abort if TOC is empty
        #feedback.pushInfo (str(TOC_dict))
        #feedback.pushInfo (str(not bool(TOC_dict)))
        
        if not bool(TOC_dict):
            raise QgsProcessingException('Invalid input value: EMPY PROJECT')
            
        
        #parametro denominazione tabella risultante
        report = 'Project_Layers_Table'
		
        fields = QgsFields()
        
        for item in i_fields:
            if item in ('Layer_N','Geometry_Not_Valid','Layer_Type','Layer_Feature_Count'):
                fields.append(QgsField(item, QVariant.Int))
            else:
                fields.append(QgsField(item, QVariant.String))
        
        
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context, fields)
        
        # If sink was not created, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSinkError method to return a standard
        # helper text for when a sink cannot be evaluated
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT)) 
            
        feat = QgsFeature()
        count = 1
        
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name().find("Project_Layers_Table") == -1:
                Layer_N = count
                count += 1
                Layer_Name = layer.name()
                Layer_Group_Level = TOC_dict.get(Layer_Name)
                Layer_Crs = layer.crs().authid()
                Layer_Source = layer.source()
                Layer_Meta_Parent_Id = layer.metadata().parentIdentifier()
                Layer_Meta_Identifier = layer.metadata().identifier()
                Layer_Meta_Title = layer.metadata().title()
                Layer_Meta_Type = layer.metadata().type()
                Layer_Meta_Language = layer.metadata().language()
                Layer_Meta_Abstract = layer.metadata().abstract()
                Raster_type = Raster_data_type = Raster_Info_dim =  '-'
                Raster_extent = Raster_Info_res = Raster_NoDataValue = '-'
                
                if layer.type() is not QgsMapLayerType.RasterLayer:
                    Layer_Feature_Count = layer.featureCount()
                    Layer_Type = layer.wkbType()
                    Layer_Storage = layer.storageType()
                    Layer_Type_Name = QgsWkbTypes.displayString(layer.wkbType())
                    
                    Geometry_Not_Valid = 0
                    for f in layer.getFeatures():
                        if not f.geometry().isGeosValid():
                            Geometry_Not_Valid += 1
                    
                else:
                    Layer_Type = (0)
                    Layer_Type_Name = QgsMapLayerType.RasterLayer.name
                    Layer_Storage = ''
                    Layer_Feature_Count = 'nan'
                    Geometry_Not_Valid = 0
                    gh = layer.height()
                    gw = layer.width()
                    Raster_extent = layer.extent().toString()
                    provider = layer.dataProvider()
                    
                    gpx = layer.rasterUnitsPerPixelX()
                    gpy = layer.rasterUnitsPerPixelY()
                    block = provider.block(1, layer.extent(),  gpy, gpx)
                    for band in range(1, layer.bandCount()+1):
                        #print('Band ', band, layer.dataProvider().sourceNoDataValue(band))
                        Raster_NoDataValue = Raster_NoDataValue + 'Band ' + str(band) + ': ' + str(layer.dataProvider().sourceNoDataValue(band)) + ' '
                        Raster_data_type = type(provider.sourceNoDataValue(band)).__name__
                        Raster_type = layer.renderer().type()
                    #feedback.pushInfo(str(gh)+' x '+str(gw)+' - '+ str(gpx)+' x '+str(gpy))  
                    Raster_Info_dim = str(gh) + ' x '+ str(gw)
                    Raster_Info_res = str(gpx) + ' x ' + str(gpy)
                       
                campi = []
                for item in i_fields:
                    campi.append(vars()[item])
                    
                feat.setAttributes(campi)
                sink.addFeature(feat, QgsFeatureSink.FastInsert)
        
        return {self.OUTPUT: dest_id}