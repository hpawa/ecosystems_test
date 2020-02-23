<template>
  <div class="container-fluid">
    <navbar></navbar>
    <div class="row">
      <div class="col">
        <h1>Groups</h1>
        <hr />
        <br />
        <br />
        <alert :message="message" v-if="showMessage"></alert>
        <b-button variant="success" @click="initForm()" v-b-modal.group-modal>Add Group</b-button>
        <b-form inline class="float-right">
          <label class="mr-sm-2" for="filter-role">Role</label>
          <b-form-select
            id="filter-role"
            class="mr-2"
            v-model="params.role"
            :options="rolesSelector"
            @change="getGroups()"
          ></b-form-select>
          <label class="mr-sm-2" for="filter-name">Group name</label>
          <b-form-input
            id="filter-name"
            placeholder="Search"
            v-model="params.name"
            @input="getGroups()"
          ></b-form-input>
        </b-form>
        <br />
        <br />
        <table class="table table-hover text-center">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Role</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(group, index) in groups" :key="index">
              <td>{{ group.name }}</td>
              <td>{{ group.role.name }}</td>
              <td>
                <b-button-group class="float-right">
                  <b-button variant="warning" @click="fillForm(group)" v-b-modal.group-modal>Update</b-button>
                  <b-button variant="danger" @click="onDeleteGroup(group)">Delete</b-button>
                  <b-button
                    variant="primary"
                    @click="fillGroupDetail(group)"
                    v-b-modal.group-detail-modal
                  >Detail</b-button>
                </b-button-group>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="groupModal" id="group-modal" :title="groupForm.title" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
          <b-form-input
            id="form-name-input"
            type="text"
            v-model="groupForm.name"
            required
            placeholder="Enter name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-role-group" label="Role:" label-for="form-role-select">
          <b-form-select
            id="form-role-select"
            v-model="groupForm.role"
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
    <b-modal ref="groupDetailModal" id="group-detail-modal" :title="'Group detail'" hide-footer>
      <b-input-group prepend="Add User">
        <b-form-select
          id="form-add-user-select"
          v-model="updGroupForm.user_id"
          :options="usersSelector"
        ></b-form-select>
        <b-input-group-append>
          <b-button variant="info" @click="updateUserGroup()">Add</b-button>
        </b-input-group-append>
      </b-input-group>      
      <b-table hover :items="usersGroup" :fields="[{'username': 'Username'}, {'role.name': 'Role'}]">        
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
      message: "",
      usersGroup: null,
      params: {
        name: null,
        group: null,
        role: null,
        order: null
      },
      showMessage: false,
      users: [],
      groups: [],
      roles: [],
      usersSelector: [],
      rolesSelector: [],
      groupsSelector: [],
      updGroupForm: {
        searchName: null,
        group_id: null,
        user_id: null
      },
      groupForm: {
        groupID: null,
        name: "",
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
      })
        .then(res => {
          this.users = res.data.users;
          this.getUsersSelector();
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
    addGroup(payload) {
      const path = "http://localhost:5000/groups";
      axios
        .post(path, payload)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    removeGroup(groupID) {
      const path = `http://localhost:5000/groups/${groupID}`;
      axios
        .delete(path)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    removeUser(userID) {
      const path = `http://localhost:5000/users/${userID}`;
      axios
        .put(path, { group_id: null })
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    updateGroup(groupID, payload) {
      const path = `http://localhost:5000/groups/${groupID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    onDeleteGroup(group) {
      this.removeGroup(group.id);
    },
    updateUserGroup() {
      const path = `http://localhost:5000/users/${this.updGroupForm.user_id}`;
      axios
        .put(path, { group_id: this.updGroupForm.group_id })
        .then(res => {
          this.updGroupForm.user_id = null,
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
          this.$refs.groupDetailModal.hide();
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
          this.$refs.groupDetailModal.hide();
        });
    },
    onDeleteUser(user) {
      this.removeUser(user.id);
      this.$refs.groupDetailModal.hide();
    },
    initForm() {
      this.groupForm.name = "";
      this.groupForm.role = null;
      this.groupForm.title = "Add Group";
      this.groupForm.method = "POST";
    },
    fillForm(group) {
      this.groupForm.name = group.name;
      this.groupForm.role = group.role.id;
      this.groupForm.title = "Update Group";
      this.groupForm.method = "PUT";
      this.groupForm.groupID = group.id;
    },
    fillGroupDetail(group) {
      this.updGroupForm.group_id = group.id;
      this.usersGroup = group.users;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.groupModal.hide();
      const payload = {
        name: this.groupForm.name,
        role_id: this.groupForm.role
      };
      if (this.groupForm.method == "POST") {
        this.addGroup(payload);
      } else if (this.groupForm.method == "PUT") {
        this.updateGroup(this.groupForm.groupID, payload);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.groupModal.hide();
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