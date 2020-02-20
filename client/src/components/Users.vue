<template>
  <div class="container-fluid">
    <navbar></navbar>
    <div class="row">
      <div class="col">
        <h1>Users</h1>
        <hr />
        <br />
        <br />
        <alert :message="message" v-if="showMessage"></alert>
        <b-button variant="success" @click="initForm()" v-b-modal.user-modal>Add User</b-button>
        <b-form inline class="float-right">
          <label class="mr-sm-2" for="filter-group">Group</label>
          <b-form-select
            id="filter-group"
            class="mr-2"
            v-model="params.group"
            :options="groupsSelector"
            @change="getUsers()"
          ></b-form-select>
          <label class="mr-sm-2" for="filter-role">Role</label>          
          <b-form-select
            id="filter-role"
            class="mr-2"            
            v-model="params.role"
            :options="rolesSelector"
            @change="getUsers()"
          ></b-form-select>
          <b-form-input                        
            placeholder="Search username"
            v-model="params.username"
            @input="getUsers()"
          ></b-form-input>
        </b-form>
        <br />
        <br />
        <table class="table table-hover text-center">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Group</th>
              <th scope="col">Role</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.username }}</td>
              <td v-if="user.group !== null">{{ user.group.name }}</td>
              <td v-else></td>
              <td v-if="user.role !== null">{{ user.role.name }}</td>
              <td>
                <b-button-group class="float-right">
                  <b-button variant="warning" @click="fillForm(user)" v-b-modal.user-modal>Update</b-button>
                  <b-button variant="danger" @click="onDeleteUser(user)">Delete</b-button>
                </b-button-group>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="userModal" id="user-modal" :title="userForm.title" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-username-group" label="Username:" label-for="form-username-input">
          <b-form-input
            id="form-username-input"
            type="text"
            v-model="userForm.username"
            required
            placeholder="Enter username"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group" label="Password:" label-for="form-password-input">
          <b-form-input
            id="form-password-input"
            type="password"
            v-model="userForm.password"
            required
            placeholder="Enter password"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-group-group" label="Group:" label-for="form-group-select">
          <b-form-select
            id="form-group-select"
            v-model="userForm.group"
            :options="groupsSelector"
            required
          ></b-form-select>
        </b-form-group>
        <b-form-group id="form-role-group" label="Role:" label-for="form-role-select">
          <b-form-select
            id="form-role-select"
            v-model="userForm.role"
            :options="rolesSelector"
            required
          ></b-form-select>
        </b-form-group>
        <b-button-group class="float-right">
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
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
      message: "",
      params: {
        username: null,
        group: null,
        role: null,
        order: null
      },
      showMessage: false,
      users: [],
      groups: [],
      roles: [],
      groupsSelector: [],
      rolesSelector: [],
      userForm: {
        userID: null,
        username: "",
        password: "",
        group: null,
        role: null,
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
        params: this.params
      })
        .then(res => {
          this.users = res.data.users;
        })
        .catch(error => {
          console.error(error);
        });
    },
    getGroups() {
      const path = "http://localhost:5000/groups";
      axios
        .get(path)
        .then(res => {
          this.groups = res.data.groups;
          this.getGroupsSelector();
        })
        .catch(error => {
          console.error(error);
        });
    },
    getRoles() {
      const path = "http://localhost:5000/roles";
      axios
        .get(path)
        .then(res => {
          this.roles = res.data.roles;
          this.getRolesSelector();
        })
        .catch(error => {
          console.error(error);
        });
    },
    getGroupsSelector() {
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
    getRolesSelector() {
      this.rolesSelector.push({ value: null, text: "Select" });
      for (let i = 0; i < this.roles.length; i++) {
        let option = {};
        for (let key in this.roles[i]) {
          if (key == "id") {
            option["value"] = this.roles[i][key];
          } else if (key == "name") {
            option["text"] = this.roles[i][key];
          }
        }
        this.rolesSelector.push(option);
      }
    },
    addUser(payload) {
      const path = "http://localhost:5000/users";
      axios
        .post(path, payload)
        .then(res => {
          this.getUsers();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getUsers();
        });
    },
    removeUser(userID) {
      const path = `http://localhost:5000/users/${userID}`;
      axios
        .delete(path)
        .then(res => {
          this.getUsers();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getUsers();
        });
    },
    updateUser(userID, payload) {
      const path = `http://localhost:5000/users/${userID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getUsers();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getUsers();
        });
    },
    onDeleteUser(user) {
      this.removeUser(user.id);
    },
    initForm() {
      this.userForm.username = "";
      this.userForm.password = "";
      this.userForm.group = null;
      this.userForm.role = null;
      this.userForm.title = "Add User";
      this.userForm.method = "POST";
    },
    fillForm(user) {
      this.userForm.username = user.username;
      this.userForm.password = user.password;
      this.userForm.group = user.group.id;
      this.userForm.role = user.role.id;
      this.userForm.title = "Update User";
      this.userForm.method = "PUT";
      this.userForm.userID = user.id;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();
      const payload = {
        username: this.userForm.username,
        password: this.userForm.username,
        group_id: this.userForm.group,
        role_id: this.userForm.role
      };
      if (this.userForm.method == "POST") {
        this.addUser(payload);
      } else if (this.userForm.method == "PUT") {
        this.updateUser(this.userForm.userID, payload);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.userModal.hide();
      this.initForm();
    }
  },
  created() {
    this.getUsers();
    this.getGroups();
    this.getRoles();
  }
};
</script>