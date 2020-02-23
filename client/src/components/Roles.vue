<template>
  <div class="container-fluid">
    <navbar></navbar>
    <div class="row">
      <div class="col">
        <h1>Roles</h1>
        <hr />
        <br />
        <br />
        <alert :message="message" v-if="showMessage"></alert>
        <b-button variant="success" @click="initForm()" v-b-modal.role-modal>Add Role</b-button>
        <b-form inline class="float-right">
        <label class="mr-sm-2" for="filter-name">Role name</label>
          <b-form-input
            id="filter-name"
            placeholder="Search"
            v-model="params.name"
            @input="getRoles()"
          ></b-form-input>
        </b-form>
        <br />
        <br />
        <table class="table table-hover text-center">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(role, index) in roles" :key="index">
              <td>{{ role.name }}</td>
              <td>
                <b-button-group class="float-right">
                  <b-button variant="warning" @click="fillForm(role)" v-b-modal.role-modal>Update</b-button>
                  <b-button variant="danger" @click="onDeleteRole(role)">Delete</b-button>
                  <b-button
                    variant="primary"
                    @click="fillRoleDetail(role)"
                    v-b-modal.role-detail-modal
                  >Detail</b-button>
                </b-button-group>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="roleModal" id="role-modal" :title="roleForm.title" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
          <b-form-input
            id="form-name-input"
            type="text"
            v-model="roleForm.name"
            required
            placeholder="Enter name"
          ></b-form-input>
        </b-form-group>
        <b-button-group class="float-right">
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="roleDetailModal" id="role-detail-modal" :title="'Role detail'" hide-footer>
      <b-input-group prepend="Add User">
        <b-form-select
          id="form-add-user-select"
          v-model="updRoleForm.user_id"
          :options="usersSelector"
        ></b-form-select>
        <b-input-group-append>
          <b-button variant="info" @click="updateUserRole()">Add</b-button>
        </b-input-group-append>
      </b-input-group>
      <b-input-group prepend="Add Group">
        <b-form-select
          id="form-add-group-select"
          v-model="updRoleForm.group_id"
          :options="groupsSelector"
        ></b-form-select>
        <b-input-group-append>
          <b-button variant="info" @click="updateGroupRole()">Add</b-button>
        </b-input-group-append>
      </b-input-group>
      <label class="mr-sm-2" for="users-list">Users list</label>
      <b-table :id="'users-list'" hover :items="usersRole" :fields="[{'username': 'Username'}, {'group.name': 'Group'}]">
      </b-table>
      <br/>
      <label class="mr-sm-2" for="groups-list">Groups list</label>
      <b-table :id="'groups-list'" hover :items="groupsRole" :fields="[{'name': 'Name'}]">
      </b-table>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import Alert from "./Alert.vue";
import NavBar from "./NavBar.vue";
export default {
  components: {
    alert: Alert,
    navbar: NavBar
  },
  data() {
    return {
      updRoleForm: {
        user_id: null,
        group_id: null,
        role_id: null, 
      },
      usersSelector: [],
      groupsSelector: [],
      usersRole: [],
      groupsRole: [],
      message: "",
      params: {
        'name': null
      },
      showMessage: false,
      roles: [],
      groups: [],
      roleForm: {
        roleID: null,
        name: "",
        title: "",
        method: ""
      }
    };
  },
  methods: {
    getUsers() {
      const path = "http://localhost:5000/users";
      axios({
        method: "GET",
        url: path,        
      })
        .then(res => {
          this.users = res.data.users;
          this.getUsersSelector();
        })
        .catch(error => {
          console.error(error);
        });
    },
    getRoles() {
      const path = "http://localhost:5000/roles";
      axios({
        method: 'GET',
        url: path,
        params: this.params
      })        
        .then(res => {
          this.roles = res.data.roles;
        })
        .catch(error => {
          console.error(error);
        });
    },
    getGroups() {
      const path = "http://localhost:5000/groups";
      axios({
        method: "GET",
        url: path,
        params: this.params
      })
        .then(res => {
          this.groups = res.data.groups;
          this.getGroupsSelector();
        })
        .catch(error => {
          console.error(error);
        });
    },
    addRole(payload) {
      const path = "http://localhost:5000/roles";
      axios
        .post(path, payload)
        .then(res => {
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
        });
    },
    removeRole(roleID) {
      const path = `http://localhost:5000/roles/${roleID}`;
      axios
        .delete(path)
        .then(res => {
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
        });
    },
    updateRole(roleID, payload) {
      const path = `http://localhost:5000/roles/${roleID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
        });
    },
    onDeleteRole(role) {
      this.removeRole(role.id);
    },
    initForm() {
      this.roleForm.name = "";
      this.roleForm.title = "Add Role";
      this.roleForm.method = "POST";
    },
    fillForm(role) {
      this.roleForm.name = role.name;
      this.roleForm.title = "Update Role";
      this.roleForm.method = "PUT";
      this.roleForm.roleID = role.id;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.roleModal.hide();
      const payload = {
        name: this.roleForm.name
      };
      if (this.roleForm.method == "POST") {
        this.addRole(payload);
      } else if (this.roleForm.method == "PUT") {
        this.updateRole(this.roleForm.roleID, payload);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.roleModal.hide();
      this.initForm();
    },
    fillRoleDetail(role) {
      this.updRoleForm.role_id = role.id;
      this.usersRole = role.users;
      this.groupsRole = role.groups;
    },
    getUsersSelector() {
      this.usersSelector = [];
      this.usersSelector.push({ value: null, text: "Select" });
      for (let i = 0; i < this.users.length; i++) {
        let option = {};
        for (let key in this.users[i]) {
          if (key == "id") {
            option["value"] = this.users[i][key];
          } else if (key == "username") {
            option["text"] = this.users[i][key];
          }
        }
        this.usersSelector.push(option);
      }
    },
    getGroupsSelector() {
      this.groupsSelector = [];
      this.groupsSelector.push({ value: null, text: "Select" });
      for (let i = 0; i < this.groups.length; i++) {
        let option = {};
        for (let key in this.groups[i]) {
          if (key == "id") {
            option["value"] = this.groups[i][key];
          } else if (key == "name") {
            option["text"] = this.groups[i][key];
          }
        }
        this.groupsSelector.push(option);
      }
    },
    updateUserRole() {
      const path = `http://localhost:5000/users/${this.updRoleForm.user_id}`;
      axios
        .put(path, { role_id: this.updRoleForm.role_id })
        .then(res => {
          this.updRoleForm.user_id = null,
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
          this.$refs.roleDetailModal.hide();
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
          this.$refs.roleDetailModal.hide();
        });
    },
    updateGroupRole() {
      const path = `http://localhost:5000/groups/${this.updRoleForm.group_id}`;
      axios
        .put(path, { role_id: this.updRoleForm.role_id })
        .then(res => {
          this.updRoleForm.group_id = null,
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
          this.$refs.roleDetailModal.hide();
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
          this.$refs.roleDetailModal.hide();
        });
    },
  },
  created() {
    this.getUsers();
    this.getRoles();
    this.getGroups();
  }
};
</script>