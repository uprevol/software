# -*- coding: utf-8 -*-
import sys

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QTreeView
from node import Node


class DictionaryTreeModel(QtCore.QAbstractItemModel):
    """Data model providing a tree of an arbitrary dictionary"""

    def __init__(self, root, parent=None):
        super(DictionaryTreeModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """the number of rows is the number of children"""
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        """Number of columns is always 2 since dictionaries consist of key-value pairs"""
        return 2

    def data(self, index, role):
        """returns the data requested by the view"""
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.data(index.column())

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """this method gets called when the user changes data"""
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setData(index.column(), value)
                return True
        return False

    def headerData(self, section, orientation, role):
        """returns the name of the requested column"""
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Key"
            if section == 1:
                return "Value"

    def flags(self, index):
        """everything is editable"""
        return (QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEditable)

    def parent(self, index):
        """returns the parent from given index"""
        node = self.getNode(index)
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        """returns an index from given row, column and parent"""
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        """returns a Node() from given index"""
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        """insert rows from starting position and number given by rows"""
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()
        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        """remove the rows from position to position+rows"""
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()
        return success

    def to_dict(self):
        return self._rootNode.to_dict()


def node_structure_from_dict(datadict, parent=None, root_node=None):
    """returns a hierarchical node stucture required by the TreeModel"""
    if not parent:
        root_node = Node('Root')
        parent = root_node

    for name, data in datadict.items():
        node = Node(name, parent)
        if isinstance(data, dict):
            node = node_structure_from_dict(data, node, root_node)
        else:
            node.value = data

    return root_node


class DictionaryTreeWidget(QtWidgets.QTreeView):
    """returns an object containing the tree of the given dictionary d.
    example:

    tree = DictionaryTree(d)
    tree.edit()
    d_edited = tree.dict()

    d_edited contains the dictionary with the edited data.
    this has to be refactored...
    """

    def __init__(self, d):
        super(DictionaryTreeWidget, self).__init__()
        self.load_dictionary(d)
    def load_dictionary(self,d):
        """load a dictionary into my tree applicatoin"""
        self._d = d
        self._nodes = node_structure_from_dict(d)
        self._model = DictionaryTreeModel(self._nodes)
        self.setModel(self._model)

    def to_dict(self):
        """returns a dictionary from the tree-data"""
        return self._model.to_dict()


class DictionaryTreeDialog(QtWidgets.QDialog):
    """guidata motivated dialog for editin dictionaries

    """

    def __init__(self, d):
        super(DictionaryTreeDialog, self).__init__()
        treeWidget = DictionaryTreeWidget(d)
        for c in range(treeWidget._model.columnCount(None)):
            treeWidget.resizeColumnToContents(c)
        self.treeWidget = treeWidget

        self.buttonOk = QtWidgets.QPushButton('Ok', self)
        self.buttonCancel = QtWidgets.QPushButton('Cancel', self)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.treeWidget)

        bhbox = QtWidgets.QHBoxLayout()
        bhbox.addStretch()
        bhbox.addWidget(self.buttonOk)
        bhbox.addWidget(self.buttonCancel)

        vbox.addLayout(bhbox)
        self.setLayout(vbox)
        self.setWindowTitle("Tree Search")
        self.setFixedWidth(600)
        self.setFixedHeight(600)

        self.connect(self.buttonOk, QtCore.SIGNAL('clicked()'), self.accept)
        self.connect(self.buttonCancel, QtCore.SIGNAL('clicked()'), self.closeCancel)

    def edit(self):
        return self.exec_()

    def to_dict(self):
        return self.treeWidget.to_dict()

    def closeCancel(self):
        d = self.treeWidget._d
        self.treeWidget.load_dictionary(d)
        self.reject()

    def closeEvent(self, event):
        self.closeCancel()


if __name__=='__main__':

    try:
        app = QtWidgets.QApplication(sys.argv)
    except:
        app = QtWidgets.qApp

    d = {
    "adm-123": {
        "admin_id": "adm-123",
        "date_of_enroll": "2021-06-07 21:26:43",
        "date_of_exit": "None",
        "name": "de",
        "password": "de",
        "sn": "1",
        "username": "de"
    },
    "apply-84d924f9-c7b7-11eb-bed2-c03eba28c61a": {
        "admin_id": "adm-123",
        "answer_date": "2021-06-09 15:49:49",
        "apply_date": "2021-06-07 23:10:58",
        "apply_id": "apply-84d924f9-c7b7-11eb-bed2-c03eba28c61a",
        "cancel_date": "None",
        "delete_status": "1",
        "rec_id": {
        "address": "joharibazar",
        "date_of_enroll": "2021-06-06 16:29:24",
        "delete_count": "15",
        "end_date": "2021-06-26",
        "image": "123",
        "location": "1232",
        "name": "dfgh",
        "phone": "4567",
        "rec_id": "rec-4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "review": "5",
        "sn": "6",
        "str_date": "2021-06-19",
        "total_delete_count": "5",
        "total_work_count": "3",
        "work_count": "16"
    },
        "recruiter_answer": "0",
        "sn": "1",
        "work_id": {
        "address": "jaipur",
        "alt_no": "12",
        "amount": "23",
        "apply_id": "apply-84d924f9-c7b7-11eb-bed2-c03eba28c61a",
        "date_of_deletion": "2021-06-17 00:00:00",
        "date_of_entry": "2021-06-07 21:26:43",
        "date_of_work": "2021-06-07 21:26:43",
        "deletion_status": "1",
        "description": "sd",
        "duration_of_work": "2",
        "location": "123",
        "rec_id": "4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "req_workers": "1",
        "sn": "1",
        "type": "abc123",
        "work_id": "work-f49407dd-c7a8-11eb-b5e0-c03eba28c61a"
    },
        "worker_id": {
        "apply_count": "13",
        "cancel_count": "23",
        "date_of_enroll": "2021-06-06 18:02:59",
        "end_date": "2021-06-26",
        "image": "546",
        "location": "965825",
        "name": "shivam gupta",
        "phone": "701421709",
        "review": "0",
        "sn": "1",
        "str_date": "2021-06-19",
        "total_apply_count": "2",
        "total_cancel_count": "4",
        "type": "abc123",
        "worker_id": "worker-542dbb52-c6c3-11eb-ae20-c03eba28c61a"
    },
        "worker_status": "0"
    },
    "rec-4156c0ae-c6b6-11eb-b279-842afdd08b0b": {
        "address": "joharibazar",
        "date_of_enroll": "2021-06-06 16:29:24",
        "delete_count": "15",
        "end_date": "2021-06-26",
        "image": "123",
        "location": "1232",
        "name": "dfgh",
        "phone": "4567",
        "rec_id": "rec-4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "review": "5",
        "sn": "6",
        "str_date": "2021-06-19",
        "total_delete_count": "5",
        "total_work_count": "3",
        "work_count": "16"
    },
    "sus-11225c7a-cf98-11eb-a725-5c3a45e9d832": {
        "action": "ert4",
        "action_date": "None",
        "action_duration": "None",
        "assigned_before": "None",
        "assigned_date": "None",
        "assigned_to": "1234",
        "message": "recruiter out of delete limit",
        "message_to_user": "None",
        "passed": "1",
        "passed_date": "2021-06-19 00:00:00",
        "passed_note": "jhdj",
        "reassigned_date": "None",
        "rec_id": {
        "address": "joharibazar",
        "date_of_enroll": "2021-06-06 16:29:24",
        "delete_count": "15",
        "end_date": "2021-06-26",
        "image": "123",
        "location": "1232",
        "name": "dfgh",
        "phone": "4567",
        "rec_id": "rec-4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "review": "5",
        "sn": "6",
        "str_date": "2021-06-19",
        "total_delete_count": "5",
        "total_work_count": "3",
        "work_count": "16"
    },
        "sn": "1",
        "sus_id": "sus-11225c7a-cf98-11eb-a725-5c3a45e9d832",
        "work_id": {
        "address": "jaipur",
        "alt_no": "12",
        "amount": "23",
        "apply_id": "apply-84d924f9-c7b7-11eb-bed2-c03eba28c61a",
        "date_of_deletion": "2021-06-17 00:00:00",
        "date_of_entry": "2021-06-07 21:26:43",
        "date_of_work": "2021-06-07 21:26:43",
        "deletion_status": "1",
        "description": "sd",
        "duration_of_work": "2",
        "location": "123",
        "rec_id": "4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "req_workers": "1",
        "sn": "1",
        "type": "abc123",
        "work_id": "work-f49407dd-c7a8-11eb-b5e0-c03eba28c61a"
    },
        "worker_id": "None"
    },
    "work-f49407dd-c7a8-11eb-b5e0-c03eba28c61a": {
        "address": "jaipur",
        "alt_no": "12",
        "amount": "23",
        "apply_id": {
        "admin_id": "adm-123",
        "answer_date": "2021-06-09 15:49:49",
        "apply_date": "2021-06-07 23:10:58",
        "apply_id": "apply-84d924f9-c7b7-11eb-bed2-c03eba28c61a",
        "cancel_date": "None",
        "delete_status": "1",
        "rec_id": {
        "address": "joharibazar",
        "date_of_enroll": "2021-06-06 16:29:24",
        "delete_count": "15",
        "end_date": "2021-06-26",
        "image": "123",
        "location": "1232",
        "name": "dfgh",
        "phone": "4567",
        "rec_id": "rec-4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "review": "5",
        "sn": "6",
        "str_date": "2021-06-19",
        "total_delete_count": "5",
        "total_work_count": "3",
        "work_count": "16"
    },
        "recruiter_answer": "0",
        "sn": "1",
        "work_id": {
        "address": "jaipur",
        "alt_no": "12",
        "amount": "23",
        "apply_id": "apply-84d924f9-c7b7-11eb-bed2-c03eba28c61a",
        "date_of_deletion": "2021-06-17 00:00:00",
        "date_of_entry": "2021-06-07 21:26:43",
        "date_of_work": "2021-06-07 21:26:43",
        "deletion_status": "1",
        "description": "sd",
        "duration_of_work": "2",
        "location": "123",
        "rec_id": "4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "req_workers": "1",
        "sn": "1",
        "type": "abc123",
        "work_id": "work-f49407dd-c7a8-11eb-b5e0-c03eba28c61a"
    },
        "worker_id": {
        "apply_count": "13",
        "cancel_count": "23",
        "date_of_enroll": "2021-06-06 18:02:59",
        "end_date": "2021-06-26",
        "image": "546",
        "location": "965825",
        "name": "shivam gupta",
        "phone": "701421709",
        "review": "0",
        "sn": "1",
        "str_date": "2021-06-19",
        "total_apply_count": "2",
        "total_cancel_count": "4",
        "type": "abc123",
        "worker_id": "worker-542dbb52-c6c3-11eb-ae20-c03eba28c61a"
    },
        "worker_status": "0"
    },
        "date_of_deletion": "2021-06-17 00:00:00",
        "date_of_entry": "2021-06-07 21:26:43",
        "date_of_work": "2021-06-07 21:26:43",
        "deletion_status": "1",
        "description": "sd",
        "duration_of_work": "2",
        "location": "123",
        "rec_id": {
        "address": "joharibazar",
        "date_of_enroll": "2021-06-06 16:29:24",
        "delete_count": "15",
        "end_date": "2021-06-26",
        "image": "123",
        "location": "1232",
        "name": "dfgh",
        "phone": "4567",
        "rec_id": "rec-4156c0ae-c6b6-11eb-b279-842afdd08b0b",
        "review": "5",
        "sn": "6",
        "str_date": "2021-06-19",
        "total_delete_count": "5",
        "total_work_count": "3",
        "work_count": "16"
    },
        "req_workers": "1",
        "sn": "1",
        "type": "abc123",
        "work_id": "work-f49407dd-c7a8-11eb-b5e0-c03eba28c61a"
    },
    "worker-542dbb52-c6c3-11eb-ae20-c03eba28c61a": {
        "apply_count": "13",
        "cancel_count": "23",
        "date_of_enroll": "2021-06-06 18:02:59",
        "end_date": "2021-06-26",
        "image": "546",
        "location": "965825",
        "name": "shivam gupta",
        "phone": "701421709",
        "review": "0",
        "sn": "1",
        "str_date": "2021-06-19",
        "total_apply_count": "2",
        "total_cancel_count": "4",
        "type": "abc123",
        "worker_id": "worker-542dbb52-c6c3-11eb-ae20-c03eba28c61a"
    }
}

    tree = DictionaryTreeDialog(d)

    if tree.edit():
        print('Accepted:')
    else:
        print('Cancelled')

    edited_dict = tree.to_dict()
    print('\nEdited dict: {}'.format(edited_dict))
    print('\nEdited dict is the same as input dict: {}'.format(edited_dict==d))
    # print('\nMy object is still of type: {}'.format(edited_dict['An Object']))
